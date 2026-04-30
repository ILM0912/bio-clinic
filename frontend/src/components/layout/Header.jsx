import React, { useState } from "react";
import Navigation from "./Navigation";
import classes from "./Header.module.css";
import butterfly from "../../assets/butterfly.png";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { BsPersonCircle, BsPerson, BsBoxArrowRight, BsBoxArrowInRight } from "react-icons/bs";
import { logout } from '../../store/store';

function Header() {
  const user = useSelector((state) => state.user);
  const [isOpen, setIsOpen] = useState(false);
  const toggleMenu = () => setIsOpen(!isOpen);
  const dispatch = useDispatch();
  const handleLogout = () => {
    dispatch(logout());
    setIsOpen(true);
  };

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
            <Link to="/login" className="btn btn-outline-primary" style={{ height: "40px" }}>
              <BsBoxArrowInRight /> Войти
            </Link>
          ) : (
            <>
              <button 
                className={classes.userBtn}
                onClick={() => toggleMenu()}
              >
                <span className={classes.userName}>
                  {user.first_name} {user.last_name?.[0]}.
                </span>
                <BsPersonCircle size={30} color="#0d6efd" />
              </button>

              {isOpen && (
                <ul className={classes.userMenu}>
                  <li>
                    <Link to="/profile" onClick={() => setIsOpen(false)}>
                      <BsPerson /> Профиль
                    </Link>
                  </li>
                  <li>
                    <Link className={classes.navLink} to="/" onClick={() => {
                        handleLogout();
                        setIsOpen(false);
                      }}
                    >
                      <BsBoxArrowRight /> Выйти
                    </Link>
                  </li>
                </ul>
              )}
            </>
          )}
        </div>

      </div>
    </header>
  );
}

export default Header;
