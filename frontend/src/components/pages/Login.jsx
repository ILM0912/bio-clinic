import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { login as loginAction } from "../../store/store";
import { useNavigate } from "react-router-dom";
import { login as loginApi } from "../../api/api";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    const user = loginApi(username, password);

    if (!user) {
      setError("Неверный логин или пароль");
      return;
    }

    dispatch(loginAction(user));
    navigate("/");
  };

  return (
    <div className="container" style={{ paddingTop: "100px", maxWidth: "400px" }}>
      <h2 className="mb-4 text-center">Вход</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          className="form-control mb-3"
          placeholder="Логин"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          className="form-control mb-3"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <div className="text-danger mb-3">{error}</div>}

        <button className="btn btn-primary w-100">
          Войти
        </button>
      </form>
    </div>
  );
};

export default Login;