import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getBranches } from "../../api/api";

const Home = () => {
  const [branches, setBranches] = useState([]);
  const [branchesError, setBranchesError] = useState("");

  useEffect(() => {
    getBranches()
      .then(setBranches)
      .catch((err) => setBranchesError(err.message));
  }, []);

  return (
    <main>
      <section
        className="bg-light border-bottom"
        style={{ padding: "70px 0" }}
      >
        <div className="container">
          <div className="text-center mx-auto" style={{ maxWidth: "760px" }}>
            <h1 className="display-5 fw-bold text-primary mb-3">
              Добро пожаловать в BioClinic
            </h1>

            <p className="lead mb-4">
              BioClinic это веб-сервис для онлайн-записи пациентов на медицинские
              услуги. На сайте можно выбрать филиал, услугу, специалиста и удобное
              время приёма.
            </p>

            <div className="d-flex justify-content-center flex-wrap gap-2">
              <Link to="/services" className="btn btn-outline-primary btn-lg">
                Выбрать услугу
              </Link>

              <Link to="/staff" className="btn btn-outline-primary btn-lg">
                Посмотреть врачей
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section style={{ padding: "55px 0" }}>
        <div className="container">
          <div className="text-center mb-4">
            <h2 className="fw-bold">Как пользоваться сайтом</h2>
            <p className="text-muted mb-0">
              Основная навигация построена вокруг выбора услуги и личного
              кабинета пользователя.
            </p>
          </div>

          <div className="row g-4">
            <div className="col-12 col-md-4">
              <div className="card h-100 shadow-sm">
                <div className="card-body">
                  <h5 className="card-title">1. Выберите услугу</h5>
                  <p className="card-text">
                    В разделе{" "}
                    <Link to="/services">Услуги</Link> можно посмотреть
                    доступные медицинские услуги и отфильтровать их по филиалу
                    или категории.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-12 col-md-4">
              <div className="card h-100 shadow-sm">
                <div className="card-body">
                  <h5 className="card-title">2. Запишитесь к врачу</h5>
                  <p className="card-text">
                    После выбора услуги сайт покажет подходящих специалистов и
                    доступное время для записи на приём.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-12 col-md-4">
              <div className="card h-100 shadow-sm">
                <div className="card-body">
                  <h5 className="card-title">3. Откройте личный кабинет</h5>
                  <p className="card-text">
                    В разделе{" "}
                    <Link to="/profile">Личный кабинет</Link> пациент видит
                    свои будущие записи и историю посещений, а врач видит
                    расписание приёмов.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-light" style={{ padding: "55px 0" }}>
        <div className="container">
          <div className="row g-4 align-items-start">
            <div className="col-12 col-lg-5">
              <h2 className="fw-bold mb-3">Филиалы BioClinic</h2>

              <p className="text-muted">
                Клиника принимает пациентов в нескольких филиалах. Перед
                записью можно выбрать удобное отделение и посмотреть услуги,
                доступные в выбранном филиале.
              </p>

              <div className="list-group shadow-sm">
                {branchesError && (
                  <div className="list-group-item text-danger">
                    {branchesError}
                  </div>
                )}

                {!branchesError && branches.length === 0 && (
                  <div className="list-group-item text-muted">
                    Филиалы пока не добавлены.
                  </div>
                )}

                {branches.map((branch) => (
                  <div className="list-group-item" key={branch.id}>
                    <h6 className="mb-1">{branch.name}</h6>

                    <p className="mb-1 text-muted">{branch.address}</p>

                    {branch.phone && (
                      <p className="mb-0 text-muted">
                        Телефон: {branch.phone}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="col-12 col-lg-7">
              <div className="card shadow-sm border-0">
                <div className="card-body p-2">
                  <iframe
                    title="Карта филиалов BioClinic"
                    src="https://yandex.ru/map-widget/v1/?um=constructor%3A9323896011e1fdc6e127be08dd570e1e57c29f966a5b82f2ea5a047f8456def4&amp;source=constructor"
                    width="100%"
                    height="420"
                    frameBorder="0"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section style={{ padding: "55px 0" }}>
        <div className="container text-center">
          <h2 className="fw-bold mb-3">Готовы записаться на приём?</h2>

          <p className="text-muted mb-4">
            Перейдите к списку услуг, выберите подходящего специалиста и
            оформите запись онлайн.
          </p>

          <Link to="/services" className="btn btn-primary btn-lg">
            Перейти к услугам
          </Link>
        </div>
      </section>
    </main>
  );
};

export default Home;