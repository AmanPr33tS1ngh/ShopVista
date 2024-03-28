"use client";
import { host_port } from "@/env";
import axios from "axios";
import { useRouter } from "next/navigation";
import { useState } from "react";

const Product = () => {
  const router = useRouter();
  const [product, setProduct] = useState({
    name: "",
    price: null,
    image: "",
    discountAmount: null,
  });
  const changeProduct = (e) => {
    setProduct({
      ...product,
      [e.target.name]: e.target.value,
    });
  };
  const createProduct = (e) => {
    e.preventDefault();
    const endpoint = `${host_port}/products/`;
    axios.post(endpoint, { product: product }).then((res) => {
      const responseData = res.data;
      if (responseData.success) router.push("/");
      console.log("res", responseData);
    });
  };

  return (
    <div className="h-screen flex justify-center items-center">
      <form className="" onSubmit={createProduct}>
        <div className="gap-6 mb-6">
          <div>
            <label
              htmlFor="username"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={product.name}
              onChange={changeProduct}
              className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              placeholder="Enter username..."
              required
            />
          </div>
        </div>
        <div className="mb-6">
          <label
            htmlFor="Price"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Price
          </label>
          <input
            type="number"
            id="price"
            name="price"
            value={product.price}
            onChange={changeProduct}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Enter price..."
            required
          />
        </div>
        <div className="mb-6">
          <label
            htmlFor="Price"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Image
          </label>
          <input
            type="text"
            id="image"
            name="image"
            value={product.image}
            onChange={changeProduct}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Enter image url..."
            required
          />
        </div>
        <div className="mb-6">
          <label
            htmlFor="Price"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Discount Amount
          </label>
          <input
            type="text"
            id="discountAmount"
            name="discountAmount"
            value={product.discountAmount}
            onChange={changeProduct}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Enter discount amount..."
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
    </div>
  );
};
export default Product;
