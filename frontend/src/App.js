import 'bootstrap/dist/css/bootstrap.min.css';
import './normalize.css'
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Home from './components/pages/Home';
import Services from './components/pages/Services';
import Appointment from './components/pages/Appointment';
import Login from "./components/pages/Login";
import Profile from './components/pages/Profile';
import Staff from './components/pages/Staff';
import { getCurrentUser } from './api/api';
import { authChecked, login, logout } from './store/store';

function App() {
  const dispatch = useDispatch();
  const isAuthChecked = useSelector((state) => state.isAuthChecked);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');

    if (!token) {
      dispatch(authChecked());
      return;
    }

    getCurrentUser()
      .then((user) => {
        dispatch(login(user));
      })
      .catch(() => {
        localStorage.removeItem('auth_token');
        dispatch(logout());
      });
  }, [dispatch]);

  if (!isAuthChecked) {
    return (
      <div className="container text-center" style={{ paddingTop: '100px' }}>
        <p className="text-muted">Проверка авторизации...</p>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Header />
      <main style={{ paddingTop: "75px" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/services" element={<Services />} />
          <Route path="/appointment/:serviceId" element={<Appointment />} />
          <Route path="/staff" element={<Staff />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
