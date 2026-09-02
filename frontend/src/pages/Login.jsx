import {
  useState
} from "react";

import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  ShieldCheck,
  Mail,
  Lock
} from "lucide-react";

import {
  useAuth
} from "../context/AuthContext";


export default function Login() {

  const {
    login
  } = useAuth();

  const navigate =
    useNavigate();


  const [
    email,
    setEmail
  ] = useState("");

  const [
    password,
    setPassword
  ] = useState("");

  const [
    error,
    setError
  ] = useState("");

  const [
    loading,
    setLoading
  ] = useState(false);


  const submit =
    async (e) => {

      e.preventDefault();

      setError("");
      setLoading(true);

      try {

        const data =
          await login(
            email,
            password
          );

        navigate(
          data.user.role === "admin"
            ? "/admin"
            : "/dashboard"
        );

      } catch (err) {

        setError(
          err.response?.data?.error ||
          "Login failed."
        );

      } finally {

        setLoading(false);

      }
    };


  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-logo">
          <ShieldCheck
            size={28}
          />
        </div>

        <h1>
          Welcome back
        </h1>

        <p>
          Sign in to SignatureVerify
        </p>


        <form
          onSubmit={submit}
        >

          <label>
            Email
          </label>

          <div className="input-wrap">
            <Mail size={17} />
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={e =>
                setEmail(
                  e.target.value
                )
              }
              required
            />
          </div>


          <label>
            Password
          </label>

          <div className="input-wrap">
            <Lock size={17} />

            <input
              type="password"
              placeholder="Your password"
              value={password}
              onChange={e =>
                setPassword(
                  e.target.value
                )
              }
              required
            />
          </div>


          {error && (
            <div className="form-error">
              {error}
            </div>
          )}


          <button
            className="auth-button"
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign in"}
          </button>

        </form>


        <div className="auth-footer">

          Don't have an account?

          <Link to="/register">
            Create account
          </Link>

        </div>

      </div>

    </div>
  );
}