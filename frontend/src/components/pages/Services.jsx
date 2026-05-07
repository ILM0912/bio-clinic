import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { getBranches, getGroups, getServices } from "../../api/api";
import ButtonFilter from "../layout/ButtonFilter";
import SelectFilter from "../layout/SelectFilter";
import ServiceItem from "./ServiceItem";

function Services() {
  const [searchParams, setSearchParams] = useSearchParams();

  const [branches, setBranches] = useState([]);
  const [groups, setGroups] = useState([]);
  const [services, setServices] = useState([]);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const selectedBranch = searchParams.get("branch")
    ? Number(searchParams.get("branch"))
    : null;

  const selectedGroup = searchParams.get("group")
    ? Number(searchParams.get("group"))
    : null;

  const visibleGroups = selectedGroup
    ? groups.filter((group) => group.id === selectedGroup)
    : groups;

  const updateFilter = (name, value) => {
    const params = new URLSearchParams(searchParams);
    if (value === null) {
      params.delete(name);
    } else {
      params.set(name, value);
    }
    setSearchParams(params);
  };

  useEffect(() => {
    Promise.all([getBranches(), getGroups()])
      .then(([branchesData, groupsData]) => {
        setBranches(branchesData);
        setGroups(groupsData);
      })
      .catch(() => {
        setError("Не удалось загрузить фильтры.");
      });
  }, []);

  useEffect(() => {
    setIsLoading(true);
    setError("");

    getServices({
      branchId: selectedBranch,
      groupId: selectedGroup,
    })
      .then((servicesData) => {
        setServices(servicesData);
      })
      .catch(() => {
        setError("Не удалось загрузить услуги.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [selectedBranch, selectedGroup]);

  return (
    <div className="container py-4">
      <h2 className="mb-4 text-primary">Наши услуги</h2>

      <div className="row g-2 mb-4 d-md-none">
        <div className="col-6">
          <SelectFilter
            id="branch-filter-mobile"
            label="Филиал"
            items={branches}
            selectedValue={selectedBranch}
            onChange={(value) => updateFilter("branch", value)}
            allLabel="Все филиалы"
          />
        </div>
        <div className="col-6">
          <SelectFilter
            id="group-filter-mobile"
            label="Категория"
            items={groups}
            selectedValue={selectedGroup}
            onChange={(value) => updateFilter("group", value)}
            allLabel="Все категории"
          />
        </div>
      </div>
      <div className="d-none d-md-block">
        <ButtonFilter
          title="Филиалы"
          items={branches}
          selectedValue={selectedBranch}
          onChange={(value) => updateFilter("branch", value)}
          allLabel="Все филиалы"
        />
        <div className="mb-4 col-12 col-md-6 col-lg-4">
          <SelectFilter
            id="group-filter"
            label="Категория услуг"
            items={groups}
            selectedValue={selectedGroup}
            onChange={(value) => updateFilter("group", value)}
            allLabel="Все категории"
          />
        </div>
      </div>

      {error && <p className="text-danger">{error}</p>}

      {isLoading && <p className="text-muted">Загрузка услуг...</p>}

      {!isLoading && services.length === 0 && !error && (
        <p className="text-muted">
          По выбранным фильтрам услуги не найдены.
        </p>
      )}

      {!isLoading &&
        visibleGroups.map((group) => {
          const groupServices = services.filter(
            (service) => service.group === group.id
          );

          if (groupServices.length === 0) {
            return null;
          }

          return (
            <div key={group.id} className="mb-5">
              <h4 className="mb-3">{group.name}</h4>

              <div className="row g-3">
                {groupServices.map((service) => (
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