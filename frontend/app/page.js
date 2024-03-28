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
    axios.get(endpoint).then((res) => {
      const responseData = res.data;
      console.log("res", responseData);
      setProducts(responseData.products);
    });
  };

  useEffect(() => {
    getAllProducts();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div>
        {console.log("prooododod", products)}
        {products.map((product) => (
          <Product {...product} />
        ))}
      </div>
    </main>
  );
}
