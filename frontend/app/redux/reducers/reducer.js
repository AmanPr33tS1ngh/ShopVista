import * as actionTypes from "../actionTypes/actionTypes";

const initialState = {
  // isAuthenticated: false,
  // accessToken: null,
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.AUTHENTICATE:
      console.log("action", action.payload);
      return {
        ...state,
        accessToken: action.payload.accessToken,
        isAuthenticated: action.payload.isAuthenticated,
      };
    default:
      return state;
  }
};

export default reducer;
