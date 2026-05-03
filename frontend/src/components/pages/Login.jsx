import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { login as loginAction } from "../../store/store";
import { login as loginApi, register as registerApi } from "../../api/api";

const Login = () => {
  const [activeTab, setActiveTab] = useState("login");

  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  const [registerEmail, setRegisterEmail] = useState("");
  const [registerFirstName, setRegisterFirstName] = useState("");
  const [registerLastName, setRegisterLastName] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const [registerPasswordConfirm, setRegisterPasswordConfirm] = useState("");

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const resetError = () => {
    setError("");
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    resetError();
  };

  const handleLoginSubmit = (event) => {
    event.preventDefault();

    setError("");
    setIsLoading(true);

    loginApi({
      email: loginEmail,
      password: loginPassword,
    })
      .then((user) => {
        dispatch(loginAction(user));
        navigate("/");
      })
      .catch((error) => {
        setError("Неверный email или пароль");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const handleRegisterSubmit = (event) => {
    event.preventDefault();

    if (registerPassword !== registerPasswordConfirm) {
      setError("Пароли не совпадают");
      setIsLoading(false);
      return;
    }

    setError("");
    setIsLoading(true);

    registerApi({
      email: registerEmail,
      first_name: registerFirstName,
      last_name: registerLastName,
      password: registerPassword,
    })
      .then(() =>
        loginApi({
          email: registerEmail,
          password: registerPassword,
        })
      )
      .then((user) => {
        dispatch(loginAction(user));
        navigate("/");
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <div className="container" style={{paddingTop: "100px", maxWidth: "500px"}}>
      <div className="card shadow-sm border-0">
        <div className="card-body p-4">
          <div className="d-flex mb-4 bg-light rounded-3 p-1">
            <button
              type="button"
              className={`btn w-50 ${
                activeTab === "login" ? "btn-primary" : "btn-light"
              }`}
              onClick={() => handleTabChange("login")}
            >
              Вход
            </button>
            <button
              type="button"
              className={`btn w-50 ${
                activeTab === "register" ? "btn-primary" : "btn-light"
              }`}
              onClick={() => handleTabChange("register")}
            >
              Регистрация
            </button>
          </div>

          {activeTab === "login" && (
            <form onSubmit={handleLoginSubmit}>
              <input
                type="email"
                className="form-control mb-3"
                placeholder="Email"
                value={loginEmail}
                onChange={(event) => setLoginEmail(event.target.value)}
                required
              />
              <input
                type="password"
                className="form-control mb-3"
                placeholder="Пароль"
                value={loginPassword}
                onChange={(event) => setLoginPassword(event.target.value)}
                required
              />
              {error && <div className="text-danger mb-3">{error}</div>}
              <button
                type="submit"
                className="btn btn-primary w-100"
                disabled={isLoading}
              >
                {isLoading ? "Вход..." : "Войти"}
              </button>
            </form>
          )}

          {activeTab === "register" && (
            <form onSubmit={handleRegisterSubmit}>
              <input
                type="text"
                className="form-control mb-3"
                placeholder="Имя"
                value={registerFirstName}
                onChange={(event) => setRegisterFirstName(event.target.value)}
                required
              />
              <input
                type="text"
                className="form-control mb-3"
                placeholder="Фамилия"
                value={registerLastName}
                onChange={(event) => setRegisterLastName(event.target.value)}
                required
              />
              <input
                type="email"
                className="form-control mb-3"
                placeholder="Email"
                value={registerEmail}
                onChange={(event) => setRegisterEmail(event.target.value)}
                required
              />
              <input
                type="password"
                className="form-control mb-3"
                placeholder="Пароль"
                value={registerPassword}
                onChange={(event) => setRegisterPassword(event.target.value)}
                required
              />
              <input
                type="password"
                className="form-control mb-3"
                placeholder="Повторите пароль"
                value={registerPasswordConfirm}
                onChange={(event) => setRegisterPasswordConfirm(event.target.value)}
                required
              />
              {error && <div className="text-danger mb-3">{error}</div>}
              <button
                type="submit"
                className="btn btn-primary w-100"
                disabled={isLoading}
              >
                {isLoading ? "Регистрация..." : "Зарегистрироваться"}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default Login;