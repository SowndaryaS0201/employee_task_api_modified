import React, { useState, useEffect } from "react";
import api, { setAuthToken } from "./api";

/*
  App flow:
  - AuthCard (flip login/signup)
  - On successful login store token in localStorage -> show Home
  - Home fetches employees/tasks using the global axios client which has Authorization header set
*/

export default function App() {
  // Use single key "token" everywhere (consistent)
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [view, setView] = useState(token ? "home" : "auth");

  // ensure axios global header is set whenever token changes
  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
      setAuthToken(token); // set header in api client
      setView("home");
    } else {
      localStorage.removeItem("token");
      setAuthToken(null);
      setView("auth");
    }
  }, [token]);

  function handleLogout() {
    setToken("");
  }

  return (
    <div className="wrapper">
      <div className="container">
        <AuthAndHome view={view} setToken={setToken} token={token} onLogout={handleLogout} />
      </div>
    </div>
  );
}

/* combined wrapper that displays Auth (left) and Home (right) */
function AuthAndHome({ view, setToken, token, onLogout }) {
  return (
    <>
      {view === "auth" && <AuthCard onLogin={setToken} />}
      {view === "home" && <Home token={token} onLogout={onLogout} />}
    </>
  );
}

/* Auth flip card: uses username instead of email */
function AuthCard({ onLogin }) {
  const [loginUser, setLoginUser] = useState("");
  const [loginPass, setLoginPass] = useState("");

  const [signName, setSignName] = useState("");
  const [signUser, setSignUser] = useState("");
  const [signPass, setSignPass] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    try {
      const token = await api.getToken(loginUser, loginPass);
      if (!token) throw new Error("No token returned");
      onLogin(token);
    } catch (err) {
      console.error("Login error:", err);
      alert("Login failed — check credentials and backend. See console for details.");
    }
  }

  async function handleSignup(e) {
    e.preventDefault();
    try {
      await api.register(signUser, signPass);
      alert("Registered successfully. Now sign in from Log in tab.");
    } catch (err) {
      console.error("Register error:", err);
      alert("Registration failed (maybe user exists). See console for details.");
    }
  }

  return (
    <div className="card-switch">
      <label className="switch">
        <input type="checkbox" className="toggle" />
        <span className="slider" />
        <span className="card-side" />

        <div className="flip-card__inner">
          <div className="flip-card__front">
            <h2 className="title">Log In</h2>
            <form className="flip-card__form" onSubmit={handleLogin}>
              <input
                required
                className="flip-card__input"
                placeholder="Username"
                value={loginUser}
                onChange={(e) => setLoginUser(e.target.value)}
              />
              <input
                required
                type="password"
                className="flip-card__input"
                placeholder="Password"
                value={loginPass}
                onChange={(e) => setLoginPass(e.target.value)}
              />
              <button className="flip-card__btn" type="submit">Let's go!</button>
            </form>
          </div>

          <div className="flip-card__back">
            <h2 className="title">Sign Up</h2>
            <form className="flip-card__form" onSubmit={handleSignup}>
              <input className="flip-card__input" placeholder="Full name" value={signName} onChange={(e) => setSignName(e.target.value)} />
              <input required className="flip-card__input" placeholder="Username" value={signUser} onChange={(e) => setSignUser(e.target.value)} />
              <input required type="password" className="flip-card__input" placeholder="Password" value={signPass} onChange={(e) => setSignPass(e.target.value)} />
              <button className="flip-card__btn" type="submit">Confirm!</button>
            </form>
          </div>
        </div>
      </label>
    </div>
  );
}

/* Simple Home placeholder - replace with your dashboard components */
function Home({ token, onLogout }) {
  const [employees, setEmployees] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    // use api functions which use the axios client (headers already set)
    Promise.all([api.listEmployees(), api.listTasks()])
      .then(([emps, ts]) => {
        setEmployees(emps || []);
        setTasks(ts || []);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        alert("Failed to load data. Check console for details.");
      })
      .finally(() => setLoading(false));
  }, [token]);

  return (
    <div className="home-panel">
      <div className="h-row">
        <div>
          <h3>Employee & Task Manager</h3>
          <div style={{ color: "var(--font-color-sub)" }}>You are signed in.</div>
        </div>
        <div>
          <button className="small-btn" onClick={onLogout}>Logout</button>
        </div>
      </div>

      <div style={{ display: "flex", gap: 12 }}>
        <div style={{ flex: 1 }}>
          <h4>Employees</h4>
          {loading ? <div className="small">Loading…</div> : null}
          <ul className="list">
            {employees.map(e => (
              <li key={e.id} className="item">
                <div>
                  <strong>{e.first_name} {e.last_name}</strong><br />
                  <small>{e.email}</small>
                </div>
                <div>{e.task_count ?? 0} tasks</div>
              </li>
            ))}
          </ul>
        </div>

        <div style={{ width: 320 }}>
          <h4>Tasks (all)</h4>
          <ul className="list">
            {tasks.map(t => (
              <li key={t.id} className="item">
                <div>
                  <strong>{t.title}</strong><br />
                  <small>{t.description}</small>
                </div>
                <div>
                  <div>{t.employee_id ?? "—"}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
