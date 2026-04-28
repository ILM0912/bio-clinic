import { createStore } from "redux";

const TOGGLE_AGREEMENT = "agreement/toggle";
const SET_USER = "auth/setUser";

const initialState = {
  accepted: false,
  user: null,
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case TOGGLE_AGREEMENT:
      return {
        ...state,
        accepted: action.payload,
      };

    case SET_USER:
      return {
        ...state,
        user: action.payload,
      };

    default:
      return state;
  }
};

export const toggleAgreement = (value) => ({
  type: TOGGLE_AGREEMENT,
  payload: value,
});

export const setUser = (user) => ({
  type: SET_USER,
  payload: user,
});

export const store = createStore(reducer);