"use client";
import { host_port } from "@/env";
import axios from "axios";
import React, { useEffect, useState } from "react";

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  useEffect(() => {
    getUserCart();
  }, []);
  const initializeRazorpay = () => {
    return new Promise((resolve) => {
      const script = document.createElement("script");
      script.src = "https://checkout.razorpay.com/v1/checkout.js";

      script.onload = () => {
        resolve(true);
      };
      script.onerror = () => {
        resolve(false);
      };

      document.body.appendChild(script);
    });
  };

  const getUserCart = () => {
    axios
      .post(`${host_port}/cart/`, { user_id: "6602fce3e27dd94993f1fb41" })
      .then((res) => {
        const responseData = res.data;
        setCartItems(responseData.cart_items);
      });
  };

  const makePayment = async () => {
    const res = await initializeRazorpay();

    if (!res) {
      alert("Razorpay SDK Failed to load");
      return;
    }

    axios
      .post(`${host_port}/get_razorpay_offer/`, { amount: 1000 })
      .then((res) => {
        const responseData = res.data;
        var options = {
          key: responseData.RAZORPAY_KEY, // Enter the Key ID generated from the Dashboard
          name: "Shop Vista pvt ltd",
          currency: "INR",
          amount: responseData.amount,
          order_id: responseData.order_id,
          description: "Payment for items",
          image: "https://manuarora.in/logo.png",
          handler: function (response) {
            alert(response.razorpay_payment_id);
            alert(response.razorpay_order_id);
            alert(response.razorpay_signature);
          },
          prefill: {
            name: "superuser",
            email: "superuser@gmail.com",
            contact: "9999999999",
          },
        };

        const paymentObject = new window.Razorpay(options);
        paymentObject.open();
      });
  };

  const removeItemFromCart = () => {};
  const changeItemInCart = () => {};
  return (
    <div className="container mx-auto mt-10">
      <div className="flex shadow-md my-10">
        <div className="w-3/4 bg-white px-10 py-10">
          <div className="flex justify-between border-b pb-8">
            <h1 className="font-semibold text-2xl">Shopping Cart</h1>
            <h2 className="font-semibold text-2xl">3 Items</h2>
          </div>
          <div className="flex mt-10 mb-5">
            <h3 className="font-semibold text-gray-600 text-xs uppercase w-2/5">
              Product Details
            </h3>
            <h3 className="font-semibold text-center text-gray-600 text-xs uppercase w-1/5">
              Quantity
            </h3>
            <h3 className="font-semibold text-center text-gray-600 text-xs uppercase w-1/5">
              Price
            </h3>
            <h3 className="font-semibold text-center text-gray-600 text-xs uppercase w-1/5">
              Total
            </h3>
          </div>
          {cartItems?.map((item) => (
            <div className="flex items-center hover:bg-gray-100 -mx-8 px-6 py-5">
              <div className="flex w-2/5">
                <div className="w-20">
                  <img className="h-24" src={item.image} alt={item.name} />
                </div>
                <div className="flex flex-col justify-between ml-4 flex-grow">
                  <span className="font-bold text-sm">{item.name}</span>
                  <span className="text-red-500 text-xs">Apple</span>
                  <button
                    onClick={() => removeItemFromCart(item)}
                    className="font-semibold hover:text-red-500 text-gray-500 text-xs text-start"
                  >
                    Remove
                  </button>
                </div>
              </div>
              <div className="flex justify-center w-1/5">
                <button onClick={() => changeItemInCart(item)}>
                  <svg
                    className="fill-current text-gray-600 w-3"
                    viewBox="0 0 448 512"
                  >
                    <path d="M416 208H32c-17.67 0-32 14.33-32 32v32c0 17.67 14.33 32 32 32h384c17.67 0 32-14.33 32-32v-32c0-17.67-14.33-32-32-32z" />
                  </svg>
                </button>
                <div className="mx-2 border text-center w-8">{item.count}</div>
                <button onClick={() => changeItemInCart(item)}>
                  <svg
                    className="fill-current text-gray-600 w-3"
                    viewBox="0 0 448 512"
                  >
                    <path d="M416 208H272V64c0-17.67-14.33-32-32-32h-32c-17.67 0-32 14.33-32 32v144H32c-17.67 0-32 14.33-32 32v32c0 17.67 14.33 32 32 32h144v144c0 17.67 14.33 32 32 32h32c17.67 0 32-14.33 32-32V304h144c17.67 0 32-14.33 32-32v-32c0-17.67-14.33-32-32-32z" />
                  </svg>
                </button>
              </div>
              <span className="text-center w-1/5 font-semibold text-sm">
                ${item.price}
              </span>
              <span className="text-center w-1/5 font-semibold text-sm">
                $400.00
              </span>
            </div>
          ))}
        </div>

        <div id="summary" className="w-1/4 px-8 py-10">
          <h1 className="font-semibold text-2xl border-b pb-8">Order Summary</h1>
          <div className="flex justify-between mt-10 mb-5">
            <span className="font-semibold text-sm uppercase">Items 3</span>
            <span className="font-semibold text-sm">590$</span>
          </div>
          <div>
            <label className="font-medium inline-block mb-3 text-sm uppercase">
              Shipping
            </label>
            <select className="block p-2 text-gray-600 w-full text-sm">
              <option>Standard shipping - $10.00</option>
            </select>
          </div>

          <div className="border-t mt-8">
            <div className="flex font-semibold justify-between py-6 text-sm uppercase">
              <span>Total cost</span>
              <span>$600</span>
            </div>
            <button
              onClick={makePayment}
              className="bg-indigo-500 font-semibold hover:bg-indigo-600 py-3 text-sm text-white uppercase w-full"
            >
              Checkout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
