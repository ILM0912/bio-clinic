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

  const role = user.roles[0];

  let content = "";

  if (role === "user") {
    content = "Это страница пользователя";
  } else if (role === "doctor") {
    content = "Это страница врача";
  } else if (role === "admin") {
    content = "Это страница администратора";
  }

  return (
    <div className="container text-center" style={{ paddingTop: "100px" }}>
      <h2>{content}</h2>
    </div>
  );
};

export default Profile;