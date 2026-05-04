export function getYearsWord(years) {
  const lastDigit = years % 10;
  const lastTwoDigits = years % 100;

  if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
    return "лет";
  }
  if (lastDigit === 1) {
    return "год";
  }
  if (lastDigit >= 2 && lastDigit <= 4) {
    return "года";
  }
  return "лет";
}