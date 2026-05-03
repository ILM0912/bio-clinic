import React, { useState } from "react";
import classes from "./Navigation.module.css";
import { Link, useNavigate } from 'react-router-dom';
import { BsList, BsX, BsPerson, BsBoxArrowRight, BsActivity, BsHospital, BsPeople, BsBoxArrowInRight } from "react-icons/bs";
import { useSelector, useDispatch } from "react-redux";
import { logout as logoutApi } from "../../api/api";
import { logout as logoutAction } from "../../store/store";

function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const toggleMenu = () => setIsOpen(!isOpen);
  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutApi().finally(() => {
      dispatch(logoutAction());
      navigate("/");
    });
    setIsOpen(true);
  };

  return (
    <div className={classes.navWrapper}>
      <ul className={`${classes.navMenu} list-unstyled`}>
        <li>
          <Link className={classes.navLink} to="/" onClick={() => setIsOpen(false)}>
            <BsHospital/> Главная
          </Link>
        </li>
        <li>
          <Link className={classes.navLink} to="/services" onClick={() => setIsOpen(false)}>
            <BsActivity/> Услуги
          </Link>
        </li>
        <li>
          <Link className={classes.navLink} to="/staff" onClick={() => setIsOpen(false)}>
            <BsPeople/> Персонал
          </Link>
        </li>
      </ul>

      <button
        className={`btn btn-primary ${classes.menuButton}`}
        onClick={toggleMenu}
        aria-label="Toggle menu"
      >
        {isOpen ? <BsX size={24} /> : <BsList size={24} />}
      </button>

      {isOpen && (
        <ul className={`${classes.mobileMenu} list-unstyled`}>
          <li>
            <Link to="/" onClick={() => setIsOpen(false)}>
              <BsHospital/> Главная
            </Link>
          </li>
          <li>
            <Link to="/services" onClick={() => setIsOpen(false)}>
              <BsActivity/> Услуги
            </Link>
          </li>
          <li>
            <Link to="/staff" onClick={() => setIsOpen(false)}>
              <BsPeople/> Персонал
            </Link>
          </li>
          <li className={classes.mobileDivider}></li>
          {!user && (
            <li>
              <Link to="/login" onClick={() => setIsOpen(false)}>
                <BsBoxArrowInRight/> Войти
              </Link>
            </li>
          )}
          {user && (
            <>
              <li>
                <Link to="/profile" onClick={() => setIsOpen(false)}>
                  <BsPerson /> {user.first_name} {user.last_name?.[0]}.
                </Link>
              </li>
              <li>
                <Link to="/" onClick={() => {
                    handleLogout();
                    setIsOpen(false);
                  }}
                >
                  <BsBoxArrowRight /> Выйти
                </Link>
              </li>
            </>
          )}
        </ul>
      )}
    </div>
  );
}

export default Navigation;
