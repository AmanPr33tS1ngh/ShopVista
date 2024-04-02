"use client";

import { Provider } from "react-redux";
import { store } from "./store";
import { persistStore } from "redux-persist";
import Navbar from "@/components/Navbar/Navbar";

persistStore(store);
export default function ReduxProvider({ children }) {
  return (
    <Provider store={store}>
      <Navbar />
      {children}
    </Provider>
  );
}
