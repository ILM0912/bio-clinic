import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import { BsBoxArrowInRight } from "react-icons/bs";

import {
  getDoctorServices,
  getService,
} from "../../api/api";
import AppointmentForm from "../layout/AppointmentForm";

function Appointment() {
  const { serviceId } = useParams();
  const user = useSelector((state) => state.user);
  const [service, setService] = useState(null);
  const [doctorServices, setDoctorServices] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setIsLoading(true);
    setError("");

    Promise.all([getService(serviceId), getDoctorServices(serviceId)])
      .then(([serviceData, doctorServicesData]) => {
        setService(serviceData);
        setDoctorServices(doctorServicesData);
      })
      .catch(() => {
        setError("Не удалось загрузить данные для записи.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [serviceId]);

  if (isLoading) {
    return (
      <div className="container py-4">
        <p className="text-muted">Загрузка формы записи...</p>
      </div>
    );
  }

  if (error && !service) {
    return (
      <div className="container py-4">
        <p className="text-danger">{error}</p>
      </div>
    );
  }

  if (!service) {
    return (
      <div className="container py-4">
        <p className="text-danger">Услуга не найдена.</p>
      </div>
    );
  }

  return (
    <div className="container py-4">
      <div className="mb-4">
        <h2 className="text-primary mb-3">
          Запись на услугу: {service.title}
        </h2>
        <p className="text-muted mb-2">{service.description}</p>
        <p className="fw-semibold mb-0">
          Стоимость: {service.price} ₽
        </p>
      </div>

      {!user ? (
        <div className="card border-0 shadow-sm">
          <div className="card-body">
            <h5 className="mb-2">Войдите, чтобы записаться на прием</h5>
            <p className="text-muted mb-3">
              Запись доступна только авторизованным пользователям.
              После входа можно будет выбрать филиал, врача, дату и время.
            </p>
            <Link to="/login" className="btn btn-outline-primary" style={{ height: "40px" }}>
              <BsBoxArrowInRight /> Войти
            </Link>
          </div>
        </div>
      ) : (
        <AppointmentForm
          doctorServices={doctorServices}
        />
      )}
    </div>
  );
}

export default Appointment;