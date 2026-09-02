import {
  useEffect,
  useState
} from "react";

import {
  CheckCircle2,
  XCircle,
  Download,
  Search
} from "lucide-react";

import API from "../api";

import Header
  from "../components/Header";


export default function History() {

  const [
    records,
    setRecords
  ] = useState([]);

  const [
    search,
    setSearch
  ] = useState("");


  useEffect(() => {

    API.get(
      "/verification/history"
    ).then(
      response => {

        setRecords(
          response.data.verifications
        );

      }
    );

  }, []);


  const filtered =
    records.filter(
      record =>
        record.filename
          .toLowerCase()
          .includes(
            search.toLowerCase()
          )
    );


  const download =
    async id => {

      const response =
        await API.get(
          `/reports/${id}/download`,
          {
            responseType:
              "blob"
          }
        );

      const url =
        window.URL.createObjectURL(
          response.data
        );

      const anchor =
        document.createElement(
          "a"
        );

      anchor.href =
        url;

      anchor.download =
        `verification-report-${id}.pdf`;

      anchor.click();

      window.URL.revokeObjectURL(
        url
      );
    };


  return (
    <>
      <Header
        title="Verification History"
      />


      <div className="page">

        <div className="page-heading">

          <div>

            <span className="eyebrow">
              RECORDS
            </span>

            <h2>
              Verification history
            </h2>

            <p>
              Review previous signature
              verification results.
            </p>

          </div>


          <div className="search-box">

            <Search
              size={16}
            />

            <input
              placeholder="Search file..."
              value={search}
              onChange={e =>
                setSearch(
                  e.target.value
                )
              }
            />

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

                <th>
                  Report
                </th>
              </tr>

            </thead>


            <tbody>

              {filtered.map(
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

                        {record.result ===
                        "Genuine"
                          ? <CheckCircle2
                              size={13}
                            />
                          : <XCircle
                              size={13}
                            />}

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


                    <td>

                      <button
                        className="table-action"
                        onClick={() =>
                          download(
                            record.id
                          )
                        }
                      >

                        <Download
                          size={15}
                        />

                        PDF

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