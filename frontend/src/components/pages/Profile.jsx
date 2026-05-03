import React from "react";
import { useSelector } from "react-redux";

const Profile = () => {
  const user = useSelector((state) => state.user);

  if (!user) {
    return (
      <div className="container text-center" style={{ paddingTop: "100px" }}>
        <h2>Вы не авторизованы</h2>
      </div>
    );
  }

  const role = user.role;

  let content = "";

  if (role === "patient") {
    content = "Это страница пациента";
  } else if (role === "doctor") {
    content = "Это страница врача";
  }

  return (
    <div className="container text-center" style={{ paddingTop: "40px" }}>
      <h2>{content}</h2>
    </div>
  );
};

export default Profile;