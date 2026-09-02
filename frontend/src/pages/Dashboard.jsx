import {
  useEffect,
  useState
} from "react";

import {
  CheckCircle2,
  XCircle,
  ShieldCheck,
  Activity
} from "lucide-react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

import API from "../api";

import Header
  from "../components/Header";

import StatCard
  from "../components/StatCard";


export default function Dashboard() {

  const [
    summary,
    setSummary
  ] = useState(null);

  const [
    chart,
    setChart
  ] = useState([]);


  useEffect(() => {

    Promise.all([
      API.get(
        "/dashboard/summary"
      ),
      API.get(
        "/dashboard/chart"
      )
    ]).then(
      ([summaryResponse, chartResponse]) => {

        setSummary(
          summaryResponse.data
        );

        setChart(
          chartResponse.data.data
        );

      }
    );

  }, []);


  return (
    <>
      <Header
        title="Dashboard"
      />


      <div className="page">

        <div className="page-heading">
          <div>
            <span className="eyebrow">
              OVERVIEW
            </span>

            <h2>
              Your verification
              workspace
            </h2>

            <p>
              Monitor signature checks,
              confidence and recent
              activity.
            </p>
          </div>
        </div>


        <div className="stats-grid">

          <StatCard
            title="Total verifications"
            value={
              summary?.total ?? "—"
            }
            subtitle="All completed checks"
            icon={ShieldCheck}
          />

          <StatCard
            title="Genuine signatures"
            value={
              summary?.genuine ?? "—"
            }
            subtitle={
              `${summary?.genuine_rate ?? 0}% genuine rate`
            }
            icon={CheckCircle2}
            className="success"
          />

          <StatCard
            title="Forged signatures"
            value={
              summary?.forged ?? "—"
            }
            subtitle="Detected as forged"
            icon={XCircle}
            className="danger"
          />

          <StatCard
            title="Average confidence"
            value={
              summary
                ? `${summary.average_confidence}%`
                : "—"
            }
            subtitle="Model confidence"
            icon={Activity}
          />

        </div>


        <div className="dashboard-card">

          <div className="card-heading">
            <div>
              <h3>
                Confidence trend
              </h3>

              <p>
                Verification confidence
                across completed checks
              </p>
            </div>
          </div>


          <div className="chart">

            <ResponsiveContainer
              width="100%"
              height={330}
            >

              <LineChart
                data={chart}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#e9edf3"
                />

                <XAxis
                  dataKey="date"
                  stroke="#8993a6"
                  fontSize={11}
                />

                <YAxis
                  stroke="#8993a6"
                  fontSize={11}
                />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="confidence"
                  stroke="#5e67d8"
                  strokeWidth={3}
                  dot={{
                    r: 4
                  }}
                />

              </LineChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>
    </>
  );
}