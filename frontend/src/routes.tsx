import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import AuthGuard from "@/components/guards/auth-guard";
import GuestGuard from "@/components/guards/guest-guard";
import AppLayout from "@/pages/app/layout";
import AuthLayout from "@/pages/auth/layout";
import Loading from "@/pages/loading.tsx";
import NotFound from "@/pages/not-found";

// Statically import all possible pages for build (matches pages/FOLDER/page.tsx)
const modules = import.meta.glob("./pages/**/page.tsx");

// Lazy load page components
const lazyLoad = (path: string) => {
  // Handle different paths based on the route
  let key: string;
  if (path.startsWith("/auth")) {
    key = `./pages/auth${path.substring(5)}/page.tsx`; // Remove "/auth"
  } else {
    key = `./pages/app${path}/page.tsx`;
  }

  const importer = modules[key];

  // If file not found fallback to 404
  if (!importer) return <Navigate to="/404" replace />;

  const Component = React.lazy(importer as () => Promise<{ default: React.ComponentType<any> }>);

  return (
    <React.Suspense fallback={<Loading />}>
      <Component />
    </React.Suspense>
  );
};

// Generate routes from file system for all app pages
const generateAppRoutesFromFiles = (): React.ReactElement[] => {
  const routes: React.ReactElement[] = [];

  for (const key in modules) {
    if (key.startsWith("./pages/app/") && key.endsWith("/page.tsx")) {
      // Extract path, e.g., "./pages/app/dashboards/default/page.tsx" -> "/dashboards/default"
      let path = key.replace("./pages/app", "").replace("/page.tsx", "");
      if (path === "") path = "/";
      routes.push(<Route key={path} path={path} element={lazyLoad(path)} />);
    }
  }

  return routes;
};

// Generate auth routes
const generateAuthRoutes = (): React.ReactElement[] => {
  return [
    <Route key="sign-in" path="sign-in" element={lazyLoad("/auth/sign-in")} />,
    <Route key="password-reset" path="password-reset" element={lazyLoad("/auth/password-reset")} />,
    <Route key="password-sent" path="password-sent" element={lazyLoad("/auth/password-sent")} />,
    <Route key="password-new" path="password-new" element={lazyLoad("/auth/password-new")} />,
    <Route key="get-verification" path="get-verification" element={lazyLoad("/auth/get-verification")} />,
    <Route key="set-verification" path="set-verification" element={lazyLoad("/auth/set-verification")} />,
    <Route key="terms-and-conditions" path="terms-and-conditions" element={lazyLoad("/auth/terms-and-conditions")} />,
    <Route key="privacy-policy" path="privacy-policy" element={lazyLoad("/auth/privacy-policy")} />,
    <Route key="ppdb-register" path="ppdb/register" element={lazyLoad("/auth/ppdb/register")} />,
    <Route key="ppdb-status" path="ppdb/status" element={lazyLoad("/auth/ppdb/status")} />,
  ];
};

const appRoutes = generateAppRoutesFromFiles();
const authRoutes = generateAuthRoutes();

// Main Routes component
const AppRoutes = () => {
  return (
    <Routes>
      {/* Auth routes with AuthLayout and GuestGuard at Root */}
      <Route
        path="/"
        element={
          <GuestGuard>
            <AuthLayout />
          </GuestGuard>
        }
      >
        <Route index element={lazyLoad("/auth/sign-in")} />
        <Route path="auth" element={<Navigate to="/" replace />} />
        {authRoutes}
      </Route>

      {/* App routes with AppLayout and AuthGuard */}
      <Route
        element={
          <AuthGuard>
            <AppLayout />
          </AuthGuard>
        }
      >
        {/* Container-level Breadcrumb Redirects to prevent 404 errors */}
        <Route path="/home" element={<Navigate to="/home/board/summary" replace />} />
        <Route path="/academic" element={<Navigate to="/academic/curriculum" replace />} />
        <Route path="/system" element={<Navigate to="/system/access" replace />} />
        <Route path="/learning" element={<Navigate to="/academic/subjects/schedule" replace />} />
        <Route path="/reports" element={<Navigate to="/reports/gradebook/scores" replace />} />
        <Route path="/profile" element={<Navigate to="/profile/school" replace />} />

        {/* Routes generated from file system */}
        {appRoutes}
        {/* Wildcard route for nested settings tabs */}
        <Route path="/settings/*" element={lazyLoad("/settings")} />
      </Route>

      {/* App routes with AppLayout and AuthGuard */}

      {/* 404 route */}
      <Route path="/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/404" replace />} />
    </Routes>
  );
};

export default AppRoutes;
