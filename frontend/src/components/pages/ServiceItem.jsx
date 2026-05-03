import React from "react";
import { Link } from "react-router-dom";

const ServiceItem = (service) => {
  const path = "/appointment/" + service.id;
  return (
    <div className="card h-100 shadow-sm mb-3">
      <div className="card-body d-flex flex-column">
        <h5 className="card-title">{service.title}</h5>
        <p className="card-text flex-grow-1">{service.description}</p>
        <Link to={path} className="btn btn-primary mt-3">
          Записаться на приём
        </Link>
      </div>
    </div>
  );
};

export default ServiceItem;
