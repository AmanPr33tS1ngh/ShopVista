"use client";
import axios from "axios";
import { useEffect, useState } from "react";
import { host_port } from "./env";
import Product from "./components/Product/Product";

export default function Home() {
  const [products, setProducts] = useState([]);
  // const makeAuthenticatedRequest = async () => {
  //   const accessToken = JSON.parse(localStorage.getItem("access_token"));
  //   console.log("access", accessToken);
  //   const authBearer = `Bearer ${accessToken}`;
  //   console.log("authBearer", authBearer);
  //   try {
  //     const options = {
  //       method: "post",
  //       headers: {
  //         Authorization: authBearer,
  //       },
  //     };
  //     const response = await fetch("http://localhost:8000/check/", options);
  //     const result = await response.json();
  //     console.log("result", result);
  //     return result;
  //     // Handle response
  //   } catch (error) {
  //     console.error("Error:", error);
  //     // Handle error
  //   }
  // };

  const getAllProducts = () => {
    const endpoint = `${host_port}/products/`;
    axios.post(endpoint).then((res) => {
      const responseData = res.data;
      setProducts(responseData.products);
    });
  };

  useEffect(() => {
    getAllProducts();
  }, []);
  const addToCart = (product) => {
    console.log("product", product);
    axios.post(`${host_port}/add_to_cart/`, {product_id: product._id, user_id: '6602fce3e27dd94993f1fb41'}).then((res)=>{
      const responseData = res.data;
      console.log('addToCart response', responseData);
    })
  };

  return (
    <main className="grid grid-cols-3 gap-3 gap-y-8 items-center justify-between p-5">
      {products?.map((product) => {
        return <Product product={...product} addToCart={addToCart} />;
      })}
    </main>
  );
}
