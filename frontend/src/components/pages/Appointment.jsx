import React from "react";
import { useParams } from "react-router-dom";
import { getService } from "../../api/api";

function Appointment() {
  const { serviceId } = useParams();
  const service = getService(serviceId);

  if (!service) {
    return <p>Услуга не найдена</p>;
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
