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

export function formatDateTime(dateTime) {
  return new Date(dateTime).toLocaleString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

export function getStatusBadgeClass(status) {
  if (status === "completed") {
    return "badge bg-success";
  }

  if (status === "cancelled") {
    return "badge bg-secondary";
  }

  return "badge bg-primary";
};