import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css"; // <- make sure this file is at src/styles.css

createRoot(document.getElementById("root")).render(<App />);

