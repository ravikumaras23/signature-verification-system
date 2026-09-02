import Header
  from "../components/Header";

import {
  useAuth
} from "../context/AuthContext";


export default function Profile() {

  const {
    user
  } = useAuth();


  return (
    <>
      <Header
        title="Profile"
      />

      <div className="page">

        <div className="profile-card">

          <div className="profile-avatar">

            {user?.name
              ?.substring(0, 2)
              .toUpperCase()}

          </div>


          <h2>
            {user?.name}
          </h2>

          <p>
            {user?.email}
          </p>


          <div className="profile-row">

            <span>
              Role
            </span>

            <strong>
              {user?.role}
            </strong>

          </div>


          <div className="profile-row">

            <span>
              Account status
            </span>

            <strong>
              {user?.is_active
                ? "Active"
                : "Disabled"}
            </strong>

          </div>


          <div className="profile-row">

            <span>
              Joined
            </span>

            <strong>
              {user?.created_at
                ? new Date(
                    user.created_at
                  ).toLocaleDateString()
                : "—"}
            </strong>

          </div>

        </div>

      </div>
    </>
  );
}