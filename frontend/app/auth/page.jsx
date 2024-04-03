"use client";

import axios from "axios";
import Head from "next/head";
import React, { useState } from "react";
import Link from "next/link";
import { AUTHENTICATE } from "@/redux/actionTypes/actionTypes";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";

const SignIn = () => {
  const router = useRouter();
  const dispatch = useDispatch();
  const [userCredentials, setUserCredentials] = useState({
    username: "",
    password: "",
  });
  const changeUserCreds = (e) => {
    setUserCredentials({
      ...userCredentials,
      [e.target.name]: e.target.value,
    });
  };

  const signIn = (e) => {
    e.preventDefault();
    const endpoint = "http://localhost:8000/sign_in/";
    axios.post(endpoint, { user: userCredentials }).then((res) => {
      const responseData = res.data;
      if (responseData.success) {
        dispatch({
          type: AUTHENTICATE,
          payload: {
            isAuthenticated: true,
          },
        });
        localStorage.setItem(
          "access_token",
          JSON.stringify(responseData.access_token)
        );
        router.push("/");
      }
    });
  };
  return (
    <div className="h-screen flex justify-center items-center">
      <Head>
        <title>Sign in</title>
      </Head>
      <div>
        <form className="" onSubmit={signIn}>
          <div className="gap-6 mb-6">
            <div>
              <label
                htmlFor="username"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Username
              </label>
              <input
                type="text"
                id="username"
                name="username"
                value={userCredentials.username}
                onChange={changeUserCreds}
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Enter username..."
                required
              />
            </div>
          </div>

          <div className="mb-6">
            <label
              htmlFor="password"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={userCredentials.password}
              onChange={changeUserCreds}
              className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              placeholder="•••••••••"
              required
            />
          </div>

          <button
            type="submit"
            className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full  px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          >
            Submit
          </button>
        </form>
        <p className="block mt-5 text-sm">
          Don't have an account?{" "}
          <Link
            className=" text-blue-500 hover:text-blue-700"
            href={"/auth/signup/"}
          >
            Sign up here
          </Link>
          .
        </p>
      </div>
    </div>
  );
};

export default SignIn;
