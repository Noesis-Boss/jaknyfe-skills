import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const api = async (path: string, options: RequestInit = {}) => {
  const response = await fetch(path, { ...options, credentials: "same-origin", headers: { "Content-Type": "application/json", ...(options.headers || {}) } });
  return response.json();
};
document.title = "Outbound workspace";

type Contact = { id: string; email: string; first_name: string | null; last_name: string | null; created_at: string };
type Campaign = { id: string; name: string; status: string; created_at: string };
type Account = { id: string; provider: string; email: string; status: string };
type EventRow = { id: string; type: string; contact_id: string | null; created_at: string };

function Dashboard() {
  const [notice, setNotice] = useState("Workspace ready");
  const [section, setSection] = useState("Overview");
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [events, setEvents] = useState<EventRow[]>([]);
  const [mockEmail, setMockEmail] = useState("");
  const [form, setForm] = useState({ name: "", subject: "", body: "" });
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadAll = async () => {
    const [c, k, a, e] = await Promise.all([api("/api/contacts"), api("/api/campaigns"), api("/api/sending-accounts"), api("/api/events")]);
    if (c.contacts) setContacts(c.contacts);
    if (k.campaigns) setCampaigns(k.campaigns);
    if (a.accounts) setAccounts(a.accounts);
    if (e.events) setEvents(e.events);
  };
  useEffect(() => { loadAll(); }, []);

  const importContacts = async (csv: string) => {
    try {
      const result = await api("/api/contacts/import", { method: "POST", headers: { "Content-Type": "text/csv" }, body: csv });
      if (result.inserted) setNotice(`${result.inserted} contact${result.inserted === 1 ? "" : "s"} imported`);
      else setNotice(result.error || "No new contacts imported");
      const fresh = await api("/api/contacts");
      if (fresh.contacts) setContacts(fresh.contacts);
    } catch { setNotice("Contact import failed. Check the CSV and try again."); }
  };
  const handleContactsFile = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) await importContacts(await file.text());
    event.target.value = "";
  };
  const createCampaign = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await api("/api/campaigns", { method: "POST", body: JSON.stringify({ name: form.name, steps: [{ subject: form.subject, body: form.body }] }) });
    if (result.id) { setNotice(`Campaign "${result.name}" created as draft`); setForm({ name: "", subject: "", body: "" }); loadAll(); }
    else setNotice(result.error || "Unable to create campaign");
  };
  const approve = async (id: string) => {
    const result = await api(`/api/campaigns/${id}/approve`, { method: "POST" });
    if (result.id) { setNotice(`Campaign "${result.name}" approved`); loadAll(); }
    else setNotice(result.error || "Unable to approve campaign");
  };
  const enrollAll = async (camp: Campaign) => {
    const ids = contacts.map(c => c.id);
    if (!ids.length) { setNotice("Import contacts before enrolling them"); return; }
    const result = await api(`/api/campaigns/${camp.id}/enroll`, { method: "POST", body: JSON.stringify({ contact_ids: ids }) });
    setNotice(result.enrolled != null ? `${result.enrolled} contact${result.enrolled === 1 ? "" : "s"} enrolled in "${camp.name}"` : result.error || "Unable to enroll contacts");
    loadAll();
  };
  const logout = async () => { await api("/api/auth/logout", { method: "POST" }); location.reload(); };
  const connectMock = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await api("/api/sending-accounts", { method: "POST", body: JSON.stringify({ provider: "mock", email: mockEmail, credentials: {} }) });
    if (result.id) { setNotice(`Test account ${result.email} connected`); setMockEmail(""); loadAll(); } else setNotice(result.error || "Unable to connect account");
  };

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const connected = params.get("connected");
    if (connected) { setNotice(`${connected === "gmail" ? "Gmail" : "Microsoft"} account connected`); window.history.replaceState({}, "", "/"); }
  }, []);

  const navItems = ["Overview", "Contacts", "Campaigns", "Sending accounts", "Events"];
  return (
    <main className="dashboard-shell">
      <aside className="rail">
        <div className="mark">SM<span>+</span></div>
        <nav>{navItems.map(name => <button type="button" className={section === name ? "active" : ""} onClick={() => setSection(name)} key={name}>{name}</button>)}</nav>
        <div className="rail-foot">v0.2 · private beta</div>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div><p className="eyebrow">SaaS-Mailer / command center</p><h1>Outbound, under control.</h1></div>
          <div className="top-actions">
            <span className="status-pill"><i /> {accounts.filter(a => a.status === "active").length} active account{accounts.filter(a => a.status === "active").length === 1 ? "" : "s"}</span>
            <button className="avatar" type="button" onClick={logout} aria-label="Sign out">DL</button>
          </div>
        </header>
        <div className="notice">{notice}<span>Authenticated workspace</span></div>

        {section === "Overview" && <>
          <section className="hero-grid">
            <article className="hero-card">
              <div className="hero-copy">
                <p className="eyebrow orange">Your next move</p>
                <h2>Turn a list into a conversation.</h2>
                <p>Import prospects, shape the sequence, and approve every send before it leaves your workspace.</p>
                <button onClick={() => fileInputRef.current?.click()}>Import contacts <b>↗</b></button>
                <input ref={fileInputRef} type="file" accept=".csv,text/csv" onChange={handleContactsFile} hidden />
              </div>
              <div className="orbit"><div className="orbit-ring ring-one" /><div className="orbit-ring ring-two" /><div className="signal">01</div></div>
            </article>
            <div className="stats">
              <article><span>Contacts</span><strong>{contacts.length || "—"}</strong><small>{contacts.length ? "in your list" : "awaiting first import"}</small></article>
              <article><span>Campaigns</span><strong>{campaigns.length || "—"}</strong><small>{campaigns.length ? `${campaigns.filter(c => c.status === "approved").length} approved` : "nothing in motion"}</small></article>
              <article><span>Events</span><strong>{events.length || "—"}</strong><small>{events.length ? "latest activity" : "no activity yet"}</small></article>
            </div>
          </section>
          <section className="lower-grid">
            <article className="panel checklist">
              <div className="panel-head"><div><p className="eyebrow">Launch sequence</p><h3>First campaign checklist</h3></div></div>
              <button type="button" className={contacts.length ? "check done" : "check"} onClick={() => setSection("Contacts")}><span>01</span><div><b>Import your contacts</b><small>Choose a CSV file from your computer.</small></div><em>{contacts.length ? "Done" : "Start"}</em></button>
              <button type="button" className={accounts.length ? "check done" : "check"} onClick={() => setSection("Sending accounts")}><span>02</span><div><b>Connect a sending account</b><small>Gmail, Outlook, or SMTP.</small></div><em>{accounts.length ? "Done" : "Start"}</em></button>
              <button type="button" className={campaigns.length ? "check done" : "check"} onClick={() => setSection("Campaigns")}><span>03</span><div><b>Draft your sequence</b><small>Write the message and timing.</small></div><em>{campaigns.length ? "Done" : "Next"}</em></button>
              <button type="button" className={campaigns.some(c => c.status === "approved") ? "check done" : "check"} onClick={() => setSection("Campaigns")}><span>04</span><div><b>Approve and send</b><small>Nothing moves without your signal.</small></div><em>{campaigns.some(c => c.status === "approved") ? "Done" : "Locked"}</em></button>
            </article>
            <article className="panel activity">
              <div className="panel-head"><div><p className="eyebrow">Live log</p><h3>Recent events</h3></div><button className="text-button" onClick={() => setSection("Events")}>View all ↗</button></div>
              {events.length ? events.slice(0, 4).map(event => <div className="event" key={event.id}><span className="event-dot" /><div><b>{event.type}</b><small>{event.contact_id || "System event"}</small></div><time>{event.created_at}</time></div>) : <div className="empty"><span>∿</span><b>No events yet</b><p>Your send history will appear here.</p></div>}
            </article>
          </section>
        </>}

        {section === "Contacts" && <section className="panel">
          <div className="panel-head"><div><p className="eyebrow">Audience</p><h3>Contacts ({contacts.length})</h3></div><button className="text-button" onClick={() => fileInputRef.current?.click()}>Import CSV ↗</button><input ref={fileInputRef} type="file" accept=".csv,text/csv" onChange={handleContactsFile} hidden /></div>
          {contacts.length ? <div className="table">{contacts.slice(0, 50).map(c => <div className="row" key={c.id}><b>{[c.first_name, c.last_name].filter(Boolean).join(" ") || "—"}</b><span>{c.email}</span></div>)}{contacts.length > 50 && <p className="table-note">Showing first 50 of {contacts.length}</p>}</div> : <div className="empty"><span>∿</span><b>No contacts yet</b><p>Import a CSV to get started.</p></div>}
        </section>}

        {section === "Campaigns" && <section className="panel">
          <div className="panel-head"><div><p className="eyebrow">Sequences</p><h3>Campaigns ({campaigns.length})</h3></div></div>
          <form className="create-campaign" onSubmit={createCampaign}>
            <input aria-label="Campaign name" placeholder="Campaign name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required />
            <input aria-label="Subject" placeholder="First email subject" value={form.subject} onChange={e => setForm({ ...form, subject: e.target.value })} required />
            <textarea aria-label="Body" placeholder="First email body" value={form.body} onChange={e => setForm({ ...form, body: e.target.value })} required />
            <button type="submit">Create draft campaign</button>
          </form>
          {campaigns.length ? campaigns.map(camp => <div className="record" key={camp.id}><div><b>{camp.name}</b><small>{camp.status} · created {camp.created_at?.slice(0, 10)}</small></div>{camp.status === "draft" && <button className="text-button" onClick={() => approve(camp.id)}>Approve ✓</button>}{camp.status !== "draft" && <button className="text-button" onClick={() => enrollAll(camp)}>Enroll contacts</button>}</div>) : <div className="empty"><span>∿</span><b>No campaigns yet</b><p>Create your first sequence above.</p></div>}
        </section>}

        {section === "Sending accounts" && <section className="panel">
          <div className="panel-head"><div><p className="eyebrow">Providers</p><h3>Sending accounts ({accounts.length})</h3></div></div>
          <div className="connect-row">
            <button type="button" onClick={() => { window.location.href = "/api/oauth/gmail/start"; }}>Connect Gmail ↗</button>
            <button type="button" onClick={() => { window.location.href = "/api/oauth/microsoft/start"; }}>Connect Microsoft ↗</button>
          </div>
          <form className="create-campaign" onSubmit={connectMock}>
            <input aria-label="Test account email" type="email" placeholder="Test account email (mock sender)" value={mockEmail} onChange={e => setMockEmail(e.target.value)} required />
            <button type="submit">Connect test account</button>
          </form>
          {accounts.length ? accounts.map(a => <div className="record" key={a.id}><b>{a.email}</b><small>{a.provider} · {a.status}</small></div>) : <div className="empty"><span>∿</span><b>No sending accounts</b><p>Connect Gmail or Microsoft via OAuth, or add a mock account for testing. Credentials stay encrypted server-side.</p></div>}
        </section>}

        {section === "Events" && <section className="panel">
          <div className="panel-head"><div><p className="eyebrow">Live log</p><h3>Events ({events.length})</h3></div><button className="text-button" onClick={loadAll}>Refresh ↻</button></div>
          {events.length ? events.map(event => <div className="event" key={event.id}><span className="event-dot" /><div><b>{event.type}</b><small>{event.contact_id || "System event"}</small></div><time>{event.created_at}</time></div>) : <div className="empty"><span>∿</span><b>No events yet</b><p>Your send history will appear here.</p></div>}
        </section>}
      </section>
    </main>
  );
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
