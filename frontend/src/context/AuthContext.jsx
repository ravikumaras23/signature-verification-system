import {
  createContext,
  useContext,
  useEffect,
  useState
} from "react";

import API from "../api";

const AuthContext =
  createContext(null);


export function AuthProvider({
  children
}) {

  const [user, setUser] =
    useState(null);

  const [loading, setLoading] =
    useState(true);


  const loadUser =
    async () => {

      const token =
        localStorage.getItem(
          "token"
        );

      if (!token) {
        setLoading(false);
        return;
      }

      try {

        const response =
          await API.get(
            "/auth/me"
          );

        setUser(
          response.data.user
        );

      } catch {

        localStorage.removeItem(
          "token"
        );

        setUser(null);

      } finally {

        setLoading(false);

      }
    };


  useEffect(() => {

    loadUser();

  }, []);


  const login =
    async (
      email,
      password
    ) => {

      const response =
        await API.post(
          "/auth/login",
          {
            email,
            password
          }
        );

      localStorage.setItem(
        "token",
        response.data.token
      );

      setUser(
        response.data.user
      );

      return response.data;
    };


  const register =
    async (
      name,
      email,
      password
    ) => {

      const response =
        await API.post(
          "/auth/register",
          {
            name,
            email,
            password
          }
        );

      localStorage.setItem(
        "token",
        response.data.token
      );

      setUser(
        response.data.user
      );

      return response.data;
    };


  const logout =
    () => {

      localStorage.removeItem(
        "token"
      );

      setUser(null);
    };


  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {

  return useContext(
    AuthContext
  );
}