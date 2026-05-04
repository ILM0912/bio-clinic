import React from "react";

const generateTimeSlots = () => {
  const slots = [];

  for (let hour = 9; hour < 17; hour += 1) {
    slots.push(`${String(hour).padStart(2, "0")}:00`);
    slots.push(`${String(hour).padStart(2, "0")}:30`);
  }

  return slots;
};

function TimeSlotPicker({ selectedValue, busySlots, onChange, disabled }) {
  const slots = generateTimeSlots();

  return (
    <div className="mb-4">
      <h5 className="mb-3">Время</h5>

      <div className="d-flex flex-wrap gap-2">
        {slots.map((slot) => {
          const isBusy = busySlots.includes(slot);
          const isSelected = selectedValue === slot;

          return (
            <button
              key={slot}
              type="button"
              disabled={disabled || isBusy}
              className={`btn ${
                isSelected ? "btn-primary" : "btn-outline-primary"
              }`}
              onClick={() => onChange(slot)}
            >
              {slot}
            </button>
          );
        })}
      </div>

      {!disabled && busySlots.length > 0 && (
        <p className="text-muted small mt-2 mb-0">
          Недоступные слоты уже заняты.
        </p>
      )}
    </div>
  );
}

export default TimeSlotPicker;