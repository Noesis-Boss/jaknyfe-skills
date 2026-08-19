import React from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function Dashboard() {
  return (
    <main className="dashboard-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">SaaS-Mailer</p>
          <h1>Outbound workspace</h1>
        </div>
        <span className="status-pill">Ready</span>
      </header>
      <section className="welcome-card">
        <p className="eyebrow">Dashboard</p>
        <h2>Build your first campaign.</h2>
        <p>Import contacts, create a sequence, and review every send from one workspace.</p>
        <button type="button">Import contacts</button>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Dashboard />
  </React.StrictMode>,
);
