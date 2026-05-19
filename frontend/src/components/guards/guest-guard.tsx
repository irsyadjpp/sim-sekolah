import { Navigate } from "react-router-dom";

export default function GuestGuard({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem("accessToken");

  if (token) {
    return <Navigate to="/home" replace />;
  }

  return <>{children}</>;
}
