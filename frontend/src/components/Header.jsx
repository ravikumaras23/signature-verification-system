import {
  Bell,
  ShieldCheck
} from "lucide-react";

import {
  useAuth
} from "../context/AuthContext";


export default function Header({
  title
}) {

  const {
    user
  } = useAuth();


  return (
    <header className="header">

      <div>

        <span className="header-label">
          WORKSPACE
        </span>

        <h1>
          {title}
        </h1>

      </div>


      <div className="header-right">

        <div className="secure-session">

          <span />

          Secure session

        </div>


        <button className="icon-btn">
          <Bell
            size={17}
          />
        </button>


        <div className="header-avatar">
          {user?.name
            ?.substring(0, 2)
            .toUpperCase()}
        </div>

      </div>

    </header>
  );
}