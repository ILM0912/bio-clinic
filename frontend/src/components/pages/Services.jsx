import React from "react";
import ServiceItem from "./ServiceItem";
import { getServices, getGroups } from "../../api/api";

function Services() {
  const services = getServices();
  const groups = getGroups();

  return (
    <div className="container py-4">
      <h2 className="mb-4 text-primary">Наши услуги</h2>
      {groups.map(group => {
        const groupServices = services.filter(s => s.groupId === group.id);
        return (
          <div key={group.id} className="mb-5">
            <h4 className="mb-3">{group.name}</h4>
            <div className="row g-3">
              {groupServices.map(service => (
                <div key={service.id} className="col-12 col-md-6 col-lg-4">
                  <ServiceItem
                    id={service.id}
                    title={service.title}
                    description={service.description}
                  />
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default Services;
