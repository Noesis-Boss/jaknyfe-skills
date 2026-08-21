import React, { useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const api = async (path: string, options: RequestInit = {}) => { const response = await fetch(path, { ...options, credentials: "same-origin", headers: { "Content-Type": "application/json", ...(options.headers || {}) } }); return response.json(); };
const dashboardLabel = "Outbound workspace";
document.title = dashboardLabel;

function Dashboard() {
  const [notice, setNotice] = useState("Workspace ready");
  const [contactCount, setContactCount] = useState(0);
  const [events, setEvents] = useState<any[]>([]);
  const [section, setSection] = useState("Overview");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const importContacts = async (csv: string) => { try { const result = await api("/api/contacts/import", { method: "POST", headers: { "Content-Type": "text/csv" }, body: csv }); setContactCount(result.inserted || 0); setNotice(result.inserted ? `${result.inserted} contact${result.inserted === 1 ? "" : "s"} imported` : result.error || "No new contacts imported"); } catch { setNotice("Contact import failed. Check the CSV and try again."); } };
  const chooseContactsFile = () => fileInputRef.current?.click();
  const handleContactsFile = async (event: React.ChangeEvent<HTMLInputElement>) => { const file = event.target.files?.[0]; if (file) await importContacts(await file.text()); event.target.value = ""; };
  const refreshEvents = async () => { const result = await api("/api/events"); setEvents(result.events || []); setNotice(`${(result.events || []).length} events in the log`); };
  const logout = async () => { await api("/api/auth/logout", { method: "POST" }); location.reload(); };
  const selectSection = (name: string) => { setSection(name); setNotice(`${name} workspace is next in the setup sequence`); };
  return <main className="dashboard-shell"><aside className="rail"><div className="mark">SM<span>+</span></div><nav>{["Overview", "Contacts", "Campaigns", "Sending accounts", "Events"].map(name => <button type="button" className={section === name ? "active" : ""} onClick={() => selectSection(name)} key={name}>{name}</button>)}</nav><div className="rail-foot">v0.1 · private beta</div></aside><section className="workspace"><header className="topbar"><div><p className="eyebrow">SaaS-Mailer / command center</p><h1>Outbound, under control.</h1></div><div className="top-actions"><span className="status-pill"><i /> All systems nominal</span><button className="avatar" type="button" onClick={logout} aria-label="Sign out">DL</button></div></header><div className="notice">{notice}<span>Authenticated workspace</span></div><section className="hero-grid"><article className="hero-card"><div className="hero-copy"><p className="eyebrow orange">Your next move</p><h2>Turn a list into a conversation.</h2><p>Import prospects, shape the sequence, and approve every send before it leaves your workspace.</p><button onClick={chooseContactsFile}>Import contacts <b>↗</b></button><input ref={fileInputRef} type="file" accept=".csv,text/csv" onChange={handleContactsFile} hidden /></div><div className="orbit"><div className="orbit-ring ring-one" /><div className="orbit-ring ring-two" /><div className="signal">01</div></div></article><div className="stats"><article><span>Contacts</span><strong>{contactCount || "—"}</strong><small>{contactCount ? "just imported" : "awaiting first import"}</small></article><article><span>Campaigns</span><strong>—</strong><small>nothing in motion</small></article><article><span>Events</span><strong>{events.length || "—"}</strong><small>{events.length ? "latest activity" : "no activity yet"}</small></article></div></section><section className="lower-grid"><article className="panel checklist"><div className="panel-head"><div><p className="eyebrow">Launch sequence</p><h3>First campaign checklist</h3></div><span className="progress">{contactCount ? "1 / 4" : "0 / 4"}</span></div><button type="button" className={contactCount ? "check done" : "check"} onClick={chooseContactsFile}><span>01</span><div><b>Import your contacts</b><small>Choose a CSV file from your computer.</small></div><em>{contactCount ? "Done" : "Start"}</em></button><button type="button" className="check" onClick={() => selectSection("Sending accounts")}><span>02</span><div><b>Connect a sending account</b><small>Gmail, Outlook, or SMTP.</small></div><em>Next</em></button><button type="button" className="check" onClick={() => selectSection("Campaigns")}><span>03</span><div><b>Draft your sequence</b><small>Write the message and timing.</small></div><em>Locked</em></button><button type="button" className="check" onClick={() => selectSection("Campaigns")}><span>04</span><div><b>Approve and send</b><small>Nothing moves without your signal.</small></div><em>Locked</em></button></article><article className="panel activity"><div className="panel-head"><div><p className="eyebrow">Live log</p><h3>Recent events</h3></div><button className="text-button" onClick={refreshEvents}>Refresh ↻</button></div>{events.length ? events.slice(0, 4).map((event) => <div className="event" key={event.id}><span className="event-dot" /><div><b>{event.type}</b><small>{event.contact_id || "System event"}</small></div><time>{event.created_at}</time></div>) : <div className="empty"><span>∿</span><b>No events yet</b><p>Your send history will appear here.</p></div>}</article></section></section></main>;
}

function Login() {
  const [registering, setRegistering] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [organizationName, setOrganizationName] = useState("");
  const [error, setError] = useState("");
  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");
    const path = registering ? "/api/auth/register" : "/api/auth/login";
    const body = registering ? { email, password, organization_name: organizationName } : { email, password };
    const result = await api(path, { method: "POST", body: JSON.stringify(body) });
    if (result.user) location.reload(); else setError(result.error || (registering ? "Unable to create account" : "Unable to log in"));
  };
  return <main className="dashboard-shell"><section className="workspace" style={{ maxWidth: 620, margin: "auto" }}><div className="panel" style={{ marginTop: "12vh" }}><p className="eyebrow orange">SaaS-Mailer</p><h1>{registering ? "Create your workspace." : "Sign in to your workspace."}</h1><form onSubmit={submit}>{registering && <input aria-label="Organization name" type="text" value={organizationName} onChange={event => setOrganizationName(event.target.value)} placeholder="Organization name" required />}<input aria-label="Email" type="email" value={email} onChange={event => setEmail(event.target.value)} placeholder="you@example.com" required /><input aria-label="Password" type="password" value={password} onChange={event => setPassword(event.target.value)} placeholder={registering ? "Password (12+ characters)" : "Password"} minLength={registering ? 12 : undefined} required /><button type="submit">{registering ? "Register new account" : "Sign in"}</button></form>{error && <p role="alert">{error}</p>}<button className="text-button auth-toggle" type="button" onClick={() => { setRegistering(!registering); setError(""); }}>{registering ? "Already have an account? Sign in" : "Register new account"}</button></div></section></main>;
}

api("/api/auth/me").then(result => createRoot(document.getElementById("root")!).render(<React.StrictMode>{result.userId ? <Dashboard /> : <Login />}</React.StrictMode>));
