"use client";
import { useState } from "react";

const Product = ({ props }) => {
  const [product, setProduct] = useState({});
  console.log("id", props);
  const getProduct = () => {};
  return (
    <div className="grid grid-cols-3 gap-3 gap-y-8 items-center justify-between p-5">
      <Product {...product} />
    </div>
  );
};
export default Product;
