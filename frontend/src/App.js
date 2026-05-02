import 'bootstrap/dist/css/bootstrap.min.css';
import './normalize.css'
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Home from './components/pages/Home';
import Services from './components/pages/Services';
import Appointment from './components/pages/Appointment';
import Login from "./components/pages/Login";
import Profile from './components/pages/Profile';
// import Staff from './components/pages/Staff';

function App() {
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
          {/* <Route path="/staff" element={<Staff />} /> */}
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
