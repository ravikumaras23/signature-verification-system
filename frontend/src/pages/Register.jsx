import {
  useState
} from "react";

import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  ShieldCheck,
  User,
  Mail,
  Lock
} from "lucide-react";

import {
  useAuth
} from "../context/AuthContext";


export default function Register() {

  const {
    register
  } = useAuth();

  const navigate =
    useNavigate();


  const [
    name,
    setName
  ] = useState("");

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
    async e => {

      e.preventDefault();

      setError("");
      setLoading(true);

      try {

        await register(
          name,
          email,
          password
        );

        navigate(
          "/dashboard"
        );

      } catch (err) {

        setError(
          err.response?.data?.error ||
          "Registration failed."
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
          Create account
        </h1>

        <p>
          Start verifying signatures
        </p>


        <form
          onSubmit={submit}
        >

          <label>
            Full name
          </label>

          <div className="input-wrap">
            <User size={17} />

            <input
              value={name}
              onChange={e =>
                setName(
                  e.target.value
                )
              }
              placeholder="Your name"
              required
            />
          </div>


          <label>
            Email
          </label>

          <div className="input-wrap">
            <Mail size={17} />

            <input
              type="email"
              value={email}
              onChange={e =>
                setEmail(
                  e.target.value
                )
              }
              placeholder="you@example.com"
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
              minLength={6}
              value={password}
              onChange={e =>
                setPassword(
                  e.target.value
                )
              }
              placeholder="Minimum 6 characters"
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
              ? "Creating..."
              : "Create account"}
          </button>

        </form>


        <div className="auth-footer">

          Already registered?

          <Link to="/login">
            Sign in
          </Link>

        </div>

      </div>

    </div>
  );
}