"use client";

import { host_port } from "@/env";
import axios from "axios";
import Link from "next/link";
import { useEffect, useState } from "react";

const Profile = () => {
  const [user, setUser] = useState(null);
  const [orderHistory, setOrderHistory] = useState([]);

  useEffect(() => {
    getProfile();
  }, []);
  const getProfile = () => {
    axios
      .post(`${host_port}/profile/`, {
        username: "superuser",
        user_id: "6602fce3e27dd94993f1fb41",
      })
      .then((res) => {
        const responseData = res.data;
        setUser(responseData.user);
        setOrderHistory(responseData.orders);
      });
  };
  return (
    <div className="container mx-auto my-28">
      <div>
        <div className="bg-white relative shadow rounded-lg mx-auto">
          <div className="flex justify-center">
            <img
              src="https://avatars0.githubusercontent.com/u/35900628?v=4"
              alt=""
              className="rounded-full mx-auto absolute -top-20 w-32 h-32 shadow-md border-4 border-white transition duration-200 transform hover:scale-110"
            />
          </div>

          <div className="mt-16">
            <h1 className="font-bold text-center text-3xl text-gray-900">
              {user?.firstName}&nbsp;{user?.lastName}
            </h1>
            <h1 className="font-bold text-center text-xl text-gray-900 my-3">
              @{user?.username}
            </h1>
            <hr />
            <h1 className=" text-center text-md text-gray-900 my-3">
              {user?.email}
            </h1>
            <h1 className=" text-center text-md text-gray-900 my-3">
              {user?.phone}
            </h1>

            {orderHistory?.length ? (
              <div className="w-full">
                <h3 className="font-medium text-gray-900 text-left px-6">
                  Recent activites
                </h3>
                {orderHistory?.map(() => (
                  <div className="mt-5 w-full flex flex-col items-center overflow-hidden text-sm">
                    <div className="w-full border-t border-gray-100 text-gray-600 py-4 pl-6 pr-3 block hover:bg-gray-100 transition duration-150">
                      <img
                        src="https://avatars0.githubusercontent.com/u/35900628?v=4"
                        alt=""
                        className="rounded-full h-6 shadow-md inline-block mr-2"
                      />
                      Updated his status
                      <span className="text-gray-500 text-xs">24 min ago</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
