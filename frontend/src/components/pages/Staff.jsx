import React, { useEffect, useState } from "react";

import { getDoctors } from "../../api/api";
import { getYearsWord } from "../../utils";

function Staff() {
  const [doctors, setDoctors] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getDoctors()
      .then((doctorsData) => {
        setDoctors(doctorsData);
      })
      .catch((requestError) => {
        setError(
          requestError.message || "Не удалось загрузить список врачей."
        );
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <div className="container py-4">
        <p className="text-muted">Загрузка специалистов...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-4">
        <p className="text-danger">{error}</p>
      </div>
    );
  }

  return (
    <div className="container py-4">
      <div className="mb-4">
        <h2 className="text-primary mb-2">Наши специалисты</h2>

        <p className="text-muted mb-0">
          Врачи клиники, доступные для консультаций, диагностики и процедур.
        </p>
      </div>

      {doctors.length === 0 ? (
        <p className="text-muted">Специалисты пока не добавлены.</p>
      ) : (
        <div className="row g-4">
          {doctors.map((doctor) => (
            <div key={doctor.id} className="col-12 col-sm-6 col-lg-4">
              <div className="card h-100 shadow-sm border-0">
                <div className="card-body text-center d-flex flex-column align-items-center">
                  {doctor.photo && (
                    <img
                      src={doctor.photo}
                      alt={`${doctor.first_name} ${doctor.last_name}`}
                      className="mb-3"
                      style={{
                        width: "120px",
                        height: "120px",
                        objectFit: "cover",
                        borderRadius: "50%",
                      }}
                    />
                  )}

                  <h5 className="card-title mb-1">
                    {doctor.first_name} {doctor.last_name}
                  </h5>

                  <p className="text-primary mb-2">
                    {doctor.specialization}
                  </p>

                  <p className="text-muted mb-0">
                    Стаж: {doctor.experience_years} {getYearsWord(doctor.experience_years)}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Staff;