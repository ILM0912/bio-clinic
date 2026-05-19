import React from "react";
import { useSelector } from "react-redux";

import PatientProfile from "./PatientProfile";
import DoctorProfile from "./DoctorProfile";

const Profile = () => {
  const user = useSelector((state) => state.user);

  if (!user) {
    return (
      <div className="container text-center" style={{ paddingTop: "100px" }}>
        <h2>Вы не авторизованы</h2>
      </div>
    );
  }

  return (
    <div className="container" style={{ paddingTop: "40px" }}>
      <h2>
        Привет, {user.first_name} {user.last_name}
      </h2>
      {user.role === "patient" && <PatientProfile user={user} />}
      {user.role === "doctor" && <DoctorProfile user={user} />}
      {user.role !== "patient" && user.role !== "doctor" && (
        <div className="text-center">
          <p className="text-muted">
            Для вашей роли личный кабинет не настроен.
          </p>
        </div>
      )}
    </div>
  );
};

export default Profile;