import axios from "axios";

const BASE = "http://127.0.0.1:8000"; // change if your backend runs elsewhere

// single axios instance so we can set Authorization header in one place
const client = axios.create({
  baseURL: BASE,
  timeout: 10000,
});

// helper to set/remove global auth header
export function setAuthToken(token) {
  if (token) {
    client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete client.defaults.headers.common["Authorization"];
  }
}

// Auth endpoints
export async function register(username, password) {
  return client.post("/auth/register", { username, password }).then(r => r.data);
}

// returns the raw access_token string
export async function getToken(username, password) {
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);
  const r = await client.post("/auth/token", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  // r.data should contain { access_token: "...", token_type: "bearer" }
  return r.data.access_token;
}

// protected endpoints that use the client (will include Authorization if set)
export async function listEmployees() {
  return client.get("/employees/").then(r => r.data);
}
export async function listTasks() {
  return client.get("/tasks/").then(r => r.data);
}

// add more wrappers if needed
export default {
  setAuthToken,
  register,
  getToken,
  listEmployees,
  listTasks,
};
