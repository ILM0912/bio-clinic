import React from "react";

function ButtonFilter({
  title,
  items,
  selectedValue,
  onChange,
  allLabel = "Все",
  showAll = true,
}) {
  return (
    <div className="mb-4">
      {title && <h5 className="mb-3">{title}</h5>}

      <div
        className="d-flex gap-2 overflow-auto pb-2"
        style={{ whiteSpace: "nowrap" }}
      >
        {showAll && (
          <button
            type="button"
            className={`btn flex-shrink-0 ${
              selectedValue === null ? "btn-primary" : "btn-outline-primary"
            }`}
            onClick={() => onChange(null)}
          >
            {allLabel}
          </button>
        )}

        {items.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`btn flex-shrink-0 ${
              selectedValue === item.id ? "btn-primary" : "btn-outline-primary"
            }`}
            onClick={() => onChange(item.id)}
          >
            {item.name}
          </button>
        ))}
      </div>
    </div>
  );
}

export default ButtonFilter;