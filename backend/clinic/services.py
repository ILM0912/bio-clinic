import random
from io import BytesIO
from pathlib import Path
from enum import Enum

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


class AvatarColor(Enum):
    BLUE = "#A8DADC"
    LIGHT_BLUE = "#BDE0FE"
    PURPLE = "#CDB4DB"
    GREEN = "#CCD5AE"
    LIME = "#D9ED92"
    ORANGE = "#F4A261"
    LAVENDER_BLUE = "#B8C0FF"
    PINK = "#FFD1DC"
    PEACH = "#FFB28B"
    LAVENDER = "#E6E6FA"


AVATAR_COLORS = [color.value for color in AvatarColor]

AVATAR_FONT_NAME = "DejaVuSans-Bold.ttf"
AVATAR_FONT_SIZE = 80
AVATAR_SIZE = (200, 200)
AVATAR_TEXT_ANCHOR = (0, 0)
AVATAR_TEXT_COLOR = "#FFFFFF"


def generate_avatar(letters, filename):
    background = random.choice(AVATAR_COLORS)
    image = Image.new("RGB", AVATAR_SIZE, background)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(AVATAR_FONT_NAME, AVATAR_FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()
    text = letters.upper()
    try:
        bbox = draw.textbbox(AVATAR_TEXT_ANCHOR, text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        x = (AVATAR_SIZE[0] - width) / 2 - bbox[0]
        y = (AVATAR_SIZE[1] - height) / 2 - bbox[1]
    except ValueError:
        width, height = draw.textsize(text, font=font)
        x = (AVATAR_SIZE[0] - width) / 2
        y = (AVATAR_SIZE[1] - height) / 2
    draw.text((x, y), text, fill=AVATAR_TEXT_COLOR, font=font)
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return ContentFile(buffer.getvalue(), name=filename)


def get_initials(user):
    first_letter = user.first_name[:1] if user.first_name else ""
    last_letter = user.last_name[:1] if user.last_name else ""
    return f"{first_letter}{last_letter}" or "DR"


def set_doctor_photo(doctor_profile, photo_name=None):
    if photo_name:
        photo_path = (
            Path(__file__).resolve().parent.parent
            / "seed_doctors"
            / photo_name
        )
        if photo_path.exists():
            with photo_path.open("rb") as photo_file:
                doctor_profile.photo.save(
                    photo_name,
                    ContentFile(photo_file.read(), name=photo_name),
                    save=True,
                )
                return
    initials = get_initials(doctor_profile.user)
    avatar = generate_avatar(
        initials,
        filename=f"doctor_{doctor_profile.user.id}_avatar.png",
    )
    doctor_profile.photo.save(
        avatar.name,
        avatar,
        save=True,
    )
