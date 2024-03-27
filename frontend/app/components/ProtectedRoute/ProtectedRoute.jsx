"use client";
import { useSelector } from "react-redux";
import Link from "next/link";
import { usePathname } from "next/navigation";

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = useSelector((state) => state.isAuthenticated);
  const pathname = usePathname();
  console.log("pathname", pathname, isAuthenticated);
  //   if (!isAuthenticated && !pathname.includes("auth")) {
  //     return <Link href="/auth">Login</Link>;
  //   }
  return children;
};

export default ProtectedRoute;
