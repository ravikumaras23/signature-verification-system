import {
  useEffect,
  useState
} from "react";

import API from "../api";

import Header
  from "../components/Header";


export default function AdminUsers() {

  const [
    users,
    setUsers
  ] = useState([]);


  const loadUsers =
    async () => {

      const response =
        await API.get(
          "/admin/users"
        );

      setUsers(
        response.data.users
      );
    };


  useEffect(() => {

    loadUsers();

  }, []);


  const toggleActive =
    async user => {

      await API.put(
        `/admin/users/${user.id}`,
        {
          is_active:
            !user.is_active
        }
      );

      loadUsers();
    };


  const changeRole =
    async (
      user,
      role
    ) => {

      await API.put(
        `/admin/users/${user.id}`,
        {
          role
        }
      );

      loadUsers();
    };


  const deleteUser =
    async id => {

      if (
        !window.confirm(
          "Delete this user?"
        )
      ) {
        return;
      }

      await API.delete(
        `/admin/users/${id}`
      );

      loadUsers();
    };


  return (
    <>
      <Header
        title="Users"
      />


      <div className="page">

        <div className="page-heading">

          <div>

            <span className="eyebrow">
              ADMINISTRATION
            </span>

            <h2>
              User management
            </h2>

            <p>
              Manage system users,
              permissions and account status.
            </p>

          </div>

        </div>


        <div className="table-card">

          <table>

            <thead>

              <tr>
                <th>
                  Name
                </th>

                <th>
                  Email
                </th>

                <th>
                  Role
                </th>

                <th>
                  Status
                </th>

                <th>
                  Actions
                </th>
              </tr>

            </thead>


            <tbody>

              {users.map(
                user => (

                  <tr
                    key={
                      user.id
                    }
                  >

                    <td>
                      {user.name}
                    </td>


                    <td>
                      {user.email}
                    </td>


                    <td>

                      <select
                        value={
                          user.role
                        }
                        onChange={e =>
                          changeRole(
                            user,
                            e.target.value
                          )
                        }
                      >

                        <option value="user">
                          User
                        </option>

                        <option value="admin">
                          Admin
                        </option>

                      </select>

                    </td>


                    <td>

                      <span
                        className={
                          `status-badge ${
                            user.is_active
                              ? "success"
                              : "danger"
                          }`
                        }
                      >
                        {user.is_active
                          ? "Active"
                          : "Disabled"}
                      </span>

                    </td>


                    <td>

                      <button
                        className="table-action"
                        onClick={() =>
                          toggleActive(
                            user
                          )
                        }
                      >
                        Toggle
                      </button>


                      <button
                        className="table-danger"
                        onClick={() =>
                          deleteUser(
                            user.id
                          )
                        }
                      >
                        Delete
                      </button>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      </div>
    </>
  );
}