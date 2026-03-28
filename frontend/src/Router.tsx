import { useRoutes } from "react-router-dom";

import Layout from "src/components/Layout";

import Home from "src/pages/Home";
import Dashboard from "src/pages/Dashboard";

export default function Router() {
  return useRoutes([
    {
      path: "/",
      element: <Layout />,
      children: [
        { index: true, element: <Home /> },
        { path: "dashboard", element: <Dashboard /> },
      ],
    },
  ]);
}
