import React, { useEffect, useState } from "react";

import {
  getAppointmentHistory,
  getUpcomingAppointments,
  updateAppointmentStatus,
} from "../../api/api";
import { formatDateTime, getStatusBadgeClass } from "../../utils";


const PatientProfile = ({ user }) => {
  const [upcomingAppointments, setUpcomingAppointments] = useState([]);
  const [historyAppointments, setHistoryAppointments] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const loadAppointments = async () => {
    setIsLoading(true);
    setError("");

    try {
      const [upcoming, history] = await Promise.all([
        getUpcomingAppointments(),
        getAppointmentHistory(),
      ]);

      setUpcomingAppointments(upcoming);
      setHistoryAppointments(history);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const reloadAppointments = async () => {
    const [upcoming, history] = await Promise.all([
      getUpcomingAppointments(),
      getAppointmentHistory(),
    ]);

    setUpcomingAppointments(upcoming);
    setHistoryAppointments(history);
  };

  useEffect(() => {
    loadAppointments();
  }, []);

  const handleCancelAppointment = async (appointmentId) => {
    const scrollY = window.scrollY;

    try {
      await updateAppointmentStatus({
        appointmentId,
        status: "cancelled",
      });

      await reloadAppointments();

      setTimeout(() => {
        window.scrollTo(0, scrollY);
      }, 0);
    } catch (err) {
      setError(err.message);
    }
  };

  const renderAppointment = (appointment, showCancelButton = false) => {
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
                <strong>Врач:</strong> {appointment.doctor_full_name}
              </p>
            </div>

            <span className={getStatusBadgeClass(appointment.status)}>
              {appointment.status_display}
            </span>
          </div>

          {showCancelButton && (
            <button
              type="button"
              className="btn btn-outline-danger btn-sm mt-3"
              onClick={() => handleCancelAppointment(appointment.id)}
            >
              Отменить запись
            </button>
          )}
        </div>
      </div>
    );
  };

  return (
    <div>
      <h2 className="mb-2">
        Привет, {user.first_name} {user.last_name}
      </h2>

      <p className="text-muted mb-4">
        Здесь отображаются будущие записи и история посещений.
      </p>

      {error && <div className="alert alert-danger">{error}</div>}

      {isLoading && <div className="alert alert-info">Загрузка записей...</div>}

      <div className="row g-4">
        <div className="col-12 col-lg-6">
          <div className="card shadow-sm h-100">
            <div className="card-header bg-white">
              <h4 className="mb-0">Будущие записи</h4>
            </div>

            <div className="card-body">
              {upcomingAppointments.length === 0 ? (
                <p className="text-muted mb-0">Будущих записей нет.</p>
              ) : (
                upcomingAppointments.map((appointment) =>
                  renderAppointment(appointment, true)
                )
              )}
            </div>
          </div>
        </div>

        <div className="col-12 col-lg-6">
          <div className="card shadow-sm h-100">
            <div className="card-header bg-white">
              <h4 className="mb-0">История записей</h4>
            </div>

            <div className="card-body">
              {historyAppointments.length === 0 ? (
                <p className="text-muted mb-0">История записей пуста.</p>
              ) : (
                historyAppointments.map((appointment) =>
                  renderAppointment(appointment)
                )
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientProfile;