import { createStore } from "redux";

const LOGIN = "auth/login";
const LOGOUT = "auth/logout";

const initialState = {
  user: null,
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case LOGIN:
      return {
        ...state,
        user: action.payload,
      };

    case LOGOUT:
      return {
        ...state,
        user: null,
      };

    default:
      return state;
  }
};

export const login = (user) => {
  return {
    type: LOGIN,
    payload: user,
  };
};

export const logout = () => ({
  type: LOGOUT,
});

export const store = createStore(reducer);