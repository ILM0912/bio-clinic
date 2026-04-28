import React, { useState } from "react";
import classes from "./Navigation.module.css";
import { Link } from 'react-router-dom';
import { BsList, BsX } from "react-icons/bs";
import { useSelector, useDispatch } from "react-redux";

function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const toggleMenu = () => setIsOpen(!isOpen);
  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const handleLogout = () => {
    // dispatch(logoutAction());
    setIsOpen(false);
  };

  return (
    <div className={classes.navWrapper}>
      <ul className={`${classes.navMenu} list-unstyled`}>
        <li>
          <Link className={classes.navLink} to="/" onClick={() => setIsOpen(false)}>Главная</Link>
        </li>
        <li>
          <Link className={classes.navLink} to="/services" onClick={() => setIsOpen(false)}>Услуги</Link>
        </li>
        <li>
          <Link className={classes.navLink} to="/staff" onClick={() => setIsOpen(false)}>Персонал</Link>
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
            <Link className={classes.navLink} to="/" onClick={() => setIsOpen(false)}>Главная</Link>
          </li>
          <li>
            <Link className={classes.navLink} to="/services" onClick={() => setIsOpen(false)}>Услуги</Link>
          </li>
          <li>
            <Link className={classes.navLink} to="/staff" onClick={() => setIsOpen(false)}>Персонал</Link>
          </li>
          {!user && (
            <li>
              <Link className={classes.navLink} to="/login" onClick={() => setIsOpen(false)}>Войти</Link>
            </li>
          )}
          {user && (
            <>
              <li className={classes.mobileDivider}></li>
              <li>
                <Link className={classes.navLink} to="/profile" onClick={() => setIsOpen(false)}>Профиль</Link>
              </li>
              <li>
                <Link className={classes.navLink} to="/" onClick={() => {
                    handleLogout();
                    setIsOpen(false);
                  }}
                >
                  Выйти
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
