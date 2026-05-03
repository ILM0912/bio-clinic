import React from "react";

function SelectFilter({
  id,
  label,
  items,
  selectedValue,
  onChange,
  allLabel = "Все",
}) {
  return (
    <div>
      {label && (
        <label htmlFor={id} className="form-label fw-semibold">
          {label}
        </label>
      )}

      <select
        id={id}
        className="form-select"
        value={selectedValue || ""}
        onChange={(event) => {
          const value = event.target.value;
          onChange(value ? Number(value) : null);
        }}
      >
        <option value="">{allLabel}</option>

        {items.map((item) => (
          <option key={item.id} value={item.id}>
            {item.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default SelectFilter;