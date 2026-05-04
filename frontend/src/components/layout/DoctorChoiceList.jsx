import React from "react";

function DoctorChoiceList({ doctors, selectedValue, onChange }) {
  if (doctors.length === 0) {
    return (
      <p className="text-muted mb-4">
        В выбранном филиале нет врачей для этой услуги.
      </p>
    );
  }

  return (
    <div className="mb-4">
      <h5 className="mb-3">Врач</h5>

      <div
        className="d-flex gap-3 overflow-auto pb-2"
        style={{ whiteSpace: "nowrap" }}
      >
        {doctors.map((item) => {
          const doctor = item.doctor;
          const isSelected = selectedValue === item.id;

          return (
            <button
              key={item.id}
              type="button"
              className={`card text-start flex-shrink-0 ${
                isSelected ? "border-primary border-2" : ""
              }`}
              style={{
                width: "280px",
                whiteSpace: "normal",
                cursor: "pointer",
              }}
              onClick={() => onChange(item.id)}
            >
              <div className="card-body d-flex gap-3 align-items-center">
                {doctor.photo && (
                  <img
                    src={doctor.photo}
                    alt={`${doctor.first_name} ${doctor.last_name}`}
                    style={{
                      width: "64px",
                      height: "64px",
                      objectFit: "cover",
                      borderRadius: "50%",
                    }}
                  />
                )}

                <div>
                  <h6 className="mb-1">
                    {doctor.first_name} {doctor.last_name}
                  </h6>

                  <p className="text-primary mb-1 small">
                    {doctor.specialization}
                  </p>

                  <p className="text-muted mb-0 small">
                    Стаж: {doctor.experience_years} лет
                  </p>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default DoctorChoiceList;