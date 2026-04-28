import React from "react";
import Navigation from "./Navigation";
import classes from "./Header.module.css";
import butterfly from "../../assets/butterfly.png";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { BsPersonCircle } from "react-icons/bs";

function Header() {
  const user = useSelector((state) => state.user);

  return (
    <header className={`${classes.header} shadow-sm`}>
      <div className="container d-flex justify-content-between align-items-center">

        <Link to="/" className="d-flex align-items-center text-decoration-none">
          <img src={butterfly} alt="BioClinic logo" className={classes.logo} />
          <h4 className={classes.brand}>BioClinic</h4>
        </Link>

        <div className={classes.navCenter}>
          <Navigation />
        </div>

        <div className={classes.authSection}>
          {!user ? (
            <Link to="/login" className="btn btn-outline-primary">
              Войти
            </Link>
          ) : (
            <Link to="/profile" className={classes.profileIcon}>
              <BsPersonCircle size={38} color="#0d6efd" />
            </Link>
          )}
        </div>

      </div>
    </header>
  );
}

export default Header;
