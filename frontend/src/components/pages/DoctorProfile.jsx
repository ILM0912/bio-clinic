import React, { useEffect, useState } from "react";

import {
  getDoctorSchedule,
  updateAppointmentStatus,
} from "../../api/api";
import { formatDateTime, getStatusBadgeClass } from "../../utils";


const DoctorProfile = ({ user }) => {
  const today = new Date().toISOString().slice(0, 10);

  const [selectedDate, setSelectedDate] = useState(today);
  const [schedule, setSchedule] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const loadSchedule = async (date) => {
    setIsLoading(true);
    setError("");

    try {
      const data = await getDoctorSchedule(date);
      setSchedule(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const reloadSchedule = async () => {
    const data = await getDoctorSchedule(selectedDate);
    setSchedule(data);
  };

  useEffect(() => {
    loadSchedule(selectedDate);
  }, [selectedDate]);

  const handleCompleteAppointment = async (appointmentId) => {
    const scrollY = window.scrollY;

    try {
      await updateAppointmentStatus({
        appointmentId,
        status: "completed",
      });

      await reloadSchedule();

      setTimeout(() => {
        window.scrollTo(0, scrollY);
      }, 0);
    } catch (err) {
      setError(err.message);
    }
  };

  const renderAppointment = (appointment) => {
    return (
      <div className="card mb-3 text-start" key={appointment.id}>
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-start gap-3">
            <div>
              <h5 className="card-title mb-2">
                {appointment.service_title}
              </h5>

              <p className="mb-1">
                <strong>Дата и время:</strong>{" "}
                {formatDateTime(appointment.date_time)}
              </p>

              <p className="mb-1">
                <strong>Филиал:</strong> {appointment.branch_name}
              </p>

              <p className="mb-1">
                <strong>Пациент:</strong> {appointment.patient_full_name}
              </p>
            </div>

            <span className={getStatusBadgeClass(appointment.status)}>
              {appointment.status_display}
            </span>
          </div>

          {appointment.status !== "completed" && (
            <button
              type="button"
              className="btn btn-outline-success btn-sm mt-3"
              onClick={() => handleCompleteAppointment(appointment.id)}
            >
              Завершить приём
            </button>
          )}
        </div>
      </div>
    );
  };

  return (
    <div>
      <p className="text-muted mb-4">
        Здесь отображается расписание приёмов на выбранную дату.
      </p>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card shadow-sm">
        <div className="card-header bg-white">
          <div className="d-flex flex-column flex-md-row justify-content-between gap-3">
            <h4 className="mb-0">Расписание врача</h4>

            <input
              type="date"
              className="form-control"
              style={{ maxWidth: "220px" }}
              value={selectedDate}
              onChange={(event) => setSelectedDate(event.target.value)}
            />
          </div>
        </div>

        <div className="card-body">
          {isLoading ? (
            <div className="alert alert-info">Загрузка расписания...</div>
          ) : schedule.length === 0 ? (
            <p className="text-muted mb-0">На выбранную дату записей нет.</p>
          ) : (
            schedule.map((appointment) => renderAppointment(appointment))
          )}
        </div>
      </div>
    </div>
  );
};

export default DoctorProfile;