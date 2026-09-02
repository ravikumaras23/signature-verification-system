import {
  useEffect,
  useState
} from "react";

import API from "../api";

import Header
  from "../components/Header";


export default function AdminVerifications() {

  const [
    records,
    setRecords
  ] = useState([]);


  useEffect(() => {

    API.get(
      "/admin/verifications"
    ).then(
      response =>
        setRecords(
          response.data.verifications
        )
    );

  }, []);


  return (
    <>
      <Header
        title="All Verifications"
      />


      <div className="page">

        <div className="page-heading">

          <div>

            <span className="eyebrow">
              ADMINISTRATION
            </span>

            <h2>
              Verification records
            </h2>

            <p>
              Review verification activity
              across all users.
            </p>

          </div>

        </div>


        <div className="table-card">

          <table>

            <thead>

              <tr>

                <th>
                  ID
                </th>

                <th>
                  User
                </th>

                <th>
                  File
                </th>

                <th>
                  Result
                </th>

                <th>
                  Confidence
                </th>

                <th>
                  Date
                </th>

              </tr>

            </thead>


            <tbody>

              {records.map(
                record => (

                  <tr
                    key={
                      record.id
                    }
                  >

                    <td>
                      #
                      {record.id}
                    </td>

                    <td>
                      <strong>
                        {record.user?.name}
                      </strong>

                      <small
                        className="table-subtitle"
                      >
                        {record.user?.email}
                      </small>
                    </td>

                    <td>
                      {record.filename}
                    </td>

                    <td>

                      <span
                        className={
                          `status-badge ${
                            record.result ===
                            "Genuine"
                              ? "success"
                              : "danger"
                          }`
                        }
                      >
                        {record.result}
                      </span>

                    </td>

                    <td>
                      {
                        record.confidence
                      }%
                    </td>

                    <td>
                      {new Date(
                        record.created_at
                      ).toLocaleString()}
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