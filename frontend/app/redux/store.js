import { createStore } from "redux";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";
import reducer from "./reducers/reducer";

// Configuration for redux-persist
const persistConfig = {
  key: "root",
  storage,
};

// Create a persisted reducer
const persistedReducer = persistReducer(persistConfig, reducer);

// Create Redux store with persisted reducer
export const store = createStore(persistedReducer);

export const persistor = persistStore(store);
