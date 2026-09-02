import {
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import ProtectedRoute
  from "./components/ProtectedRoute";

import Sidebar
  from "./components/Sidebar";

import Login
  from "./pages/Login";

import Register
  from "./pages/Register";

import Dashboard
  from "./pages/Dashboard";

import Verify
  from "./pages/Verify";

import History
  from "./pages/History";

import Reports
  from "./pages/Reports";

import Profile
  from "./pages/Profile";

import AdminDashboard
  from "./pages/AdminDashboard";

import AdminUsers
  from "./pages/AdminUsers";

import AdminVerifications
  from "./pages/AdminVerifications";

import AdminRetrain
  from "./pages/AdminRetrain";


function Layout() {

  return (
    <div className="app-layout">

      <Sidebar />

      <main className="main-area">

        <Routes>

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/verify"
            element={<Verify />}
          />

          
          <Route
            path="/admin/retrain"
            element={<AdminRetrain />}
          />


          <Route
            path="/history"
            element={<History />}
          />

          <Route
            path="/reports"
            element={<Reports />}
          />

          <Route
            path="/profile"
            element={<Profile />}
          />

          <Route
            path="/admin"
            element={<AdminDashboard />}
          />

          <Route
            path="/admin/users"
            element={<AdminUsers />}
          />

          <Route
            path="/admin/verifications"
            element={<AdminVerifications />}
          />

        </Routes>

      </main>

    </div>
  );
}


export default function App() {

  return (

    <Routes>

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />


      <Route element={<ProtectedRoute />}>

        <Route
          path="/*"
          element={<Layout />}
        />

      </Route>


      <Route
        path="/"
        element={
          <Navigate
            to="/dashboard"
            replace
          />
        }
      />

    </Routes>
  );
}