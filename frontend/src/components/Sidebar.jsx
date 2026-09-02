import {
  NavLink,
  useNavigate
} from "react-router-dom";

import {
  LayoutDashboard,
  ShieldCheck,
  History,
  FileText,
  User,
  Users,
  Settings,
  LogOut,
  Brain
} from "lucide-react";

import {
  useAuth
} from "../context/AuthContext";


export default function Sidebar() {

  const {
    user,
    logout
  } = useAuth();

  const navigate =
    useNavigate();


  const doLogout =
    () => {

      logout();

      navigate(
        "/login"
      );
    };


  return (
    <aside className="sidebar">

      <div className="brand">

        <div className="brand-logo">
          <ShieldCheck
            size={23}
          />
        </div>

        <div>
          <h2>
            Signature
            <span>
              Verify
            </span>
          </h2>

          <small>
            AI Security Platform
          </small>
        </div>

      </div>


      <div className="menu-title">
        WORKSPACE
      </div>


      <nav>

        <NavLink
          to="/dashboard"
          className="nav-link"
        >
          <LayoutDashboard
            size={18}
          />
          Dashboard
        </NavLink>


        <NavLink
          to="/verify"
          className="nav-link"
        >
          <ShieldCheck
            size={18}
          />
          Verify Signature
        </NavLink>



        <NavLink
          to="/admin/retrain"
          className="nav-link"
        >
          <Brain size={18} />
            Retrain Model
        </NavLink>


        <NavLink
          to="/history"
          className="nav-link"
        >
          <History
            size={18}
          />
          History
        </NavLink>


        <NavLink
          to="/reports"
          className="nav-link"
        >
          <FileText
            size={18}
          />
          Reports
        </NavLink>


        <NavLink
          to="/profile"
          className="nav-link"
        >
          <User
            size={18}
          />
          Profile
        </NavLink>

      </nav>


      {user?.role === "admin" && (
        <>
          <div className="menu-title admin-title">
            ADMINISTRATION
          </div>

          <nav>

            <NavLink
              to="/admin"
              className="nav-link"
            >
              <Settings
                size={18}
              />
              Admin Dashboard
            </NavLink>


            <NavLink
              to="/admin/users"
              className="nav-link"
            >
              <Users
                size={18}
              />
              Users
            </NavLink>


            <NavLink
              to="/admin/verifications"
              className="nav-link"
            >
              <ShieldCheck
                size={18}
              />
              All Verifications
            </NavLink>

          </nav>
        </>
      )}


      <div className="sidebar-bottom">

        <div className="sidebar-user">

          <div className="avatar">
            {user?.name
              ?.substring(0, 2)
              .toUpperCase()}
          </div>

          <div>

            <strong>
              {user?.name}
            </strong>

            <small>
              {user?.role}
            </small>

          </div>

        </div>


        <button
          className="logout-btn"
          onClick={doLogout}
        >
          <LogOut
            size={17}
          />
          Logout
        </button>

      </div>

    </aside>
  );
}