import {
  useEffect,
  useState
} from "react";

import {
  Users,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  Activity
} from "lucide-react";

import API from "../api";

import Header
  from "../components/Header";

import StatCard
  from "../components/StatCard";


export default function AdminDashboard() {

  const [
    data,
    setData
  ] = useState(null);


  useEffect(() => {

    API.get(
      "/admin/dashboard"
    ).then(
      response =>
        setData(
          response.data
        )
    );

  }, []);


  return (
    <>
      <Header
        title="Admin Dashboard"
      />


      <div className="page">

        <div className="page-heading">

          <div>

            <span className="eyebrow">
              ADMINISTRATION
            </span>

            <h2>
              System overview
            </h2>

            <p>
              Monitor users, verification
              activity and model results.
            </p>

          </div>

        </div>


        <div className="stats-grid">

          <StatCard
            title="Total users"
            value={
              data?.users ?? "—"
            }
            subtitle="Registered accounts"
            icon={Users}
          />

          <StatCard
            title="Total verifications"
            value={
              data?.verifications ?? "—"
            }
            subtitle="System-wide"
            icon={ShieldCheck}
          />

          <StatCard
            title="Genuine"
            value={
              data?.genuine ?? "—"
            }
            subtitle="Verified signatures"
            icon={CheckCircle2}
            className="success"
          />

          <StatCard
            title="Forged"
            value={
              data?.forged ?? "—"
            }
            subtitle="Detected signatures"
            icon={XCircle}
            className="danger"
          />

          <StatCard
            title="Average confidence"
            value={
              data
                ? `${data.average_confidence}%`
                : "—"
            }
            subtitle="System average"
            icon={Activity}
          />

        </div>

      </div>
    </>
  );
}