import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getService } from "../../api/api";

function Appointment() {
  const { serviceId } = useParams();

  const [service, setService] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setIsLoading(true);
    setError("");

    getService(serviceId)
      .then((serviceData) => {
        setService(serviceData);
      })
      .catch(() => {
        setError("Услуга не найдена.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [serviceId]);

  if (isLoading) {
    return (
      <div className="container py-4">
        <p className="text-muted">Загрузка услуги...</p>
      </div>
    );
  }

  if (error || !service) {
    return (
      <div className="container py-4">
        <p className="text-danger">{error || "Услуга не найдена."}</p>
      </div>
    );
  }

  return (
    <div className="container py-4">
      <h2 className="text-primary">Запись на услугу: {service.title}</h2>
      <p>{service.description}</p>
      <p>Здесь будет форма записи на приём.</p>
    </div>
  );
}

export default Appointment;