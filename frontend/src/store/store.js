import { createStore } from "redux";

const LOGIN = "auth/login";
const LOGOUT = "auth/logout";
const AUTH_CHECKED = "auth/checked";

const initialState = {
  user: null,
  isAuthChecked: false,
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case LOGIN:
      return {
        ...state,
        user: action.payload,
        isAuthChecked: true,
      };

    case LOGOUT:
      return {
        ...state,
        user: null,
        isAuthChecked: true,
      };

    case AUTH_CHECKED:
      return {
        ...state,
        isAuthChecked: true,
      };

    default:
      return state;
  }
};

export const login = (user) => ({
  type: LOGIN,
  payload: user,
});

export const logout = () => ({
  type: LOGOUT,
});

export const authChecked = () => ({
  type: AUTH_CHECKED,
});

export const store = createStore(reducer);