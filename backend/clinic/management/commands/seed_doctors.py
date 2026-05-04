from django.core.management.base import BaseCommand

from clinic.models import DoctorBranchService, DoctorProfile, User
from clinic.services import set_doctor_photo
from .doctors import DOCTORS


class Command(BaseCommand):
    help = "Create test doctors with photos and service assignments."

    def handle(self, *args, **options):
        for doctor_data in DOCTORS:
            user, _ = User.objects.update_or_create(
                email=doctor_data["email"],
                defaults={
                    "first_name": doctor_data["first_name"],
                    "last_name": doctor_data["last_name"],
                    "role": User.ROLE_DOCTOR,
                    "is_active": True,
                },
            )
            user.set_password(doctor_data["password"])
            user.save()
            doctor_profile, _ = DoctorProfile.objects.update_or_create(
                user=user,
                defaults={
                    "specialization": doctor_data["specialization"],
                    "work_started_at": doctor_data["work_started_at"],
                    "is_active": True,
                },
            )

            set_doctor_photo(
                doctor_profile=doctor_profile,
                photo_name=doctor_data.get("photo"),
            )

            for branch_service_id in doctor_data["branch_services"]:
                DoctorBranchService.objects.update_or_create(
                    doctor=doctor_profile,
                    branch_service_id=branch_service_id,
                    defaults={
                        "is_active": True,
                    },
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created doctor: {user.first_name} {user.last_name}"
                )
            )

        self.stdout.write(self.style.SUCCESS("Doctors seed completed."))
