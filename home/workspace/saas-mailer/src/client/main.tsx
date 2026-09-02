import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const api = async (path: string, options: RequestInit = {}) => {
  const headers = new Headers(options.headers);
  if (!(options.body instanceof FormData) && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(path, { ...options, credentials: "same-origin", headers });
  return response.json();
};
document.title = "Outbound workspace";

type Contact = { id: string; email: string; first_name: string | null; last_name: string | null; created_at: string };
type Campaign = { id: string; name: string; status: string; created_at: string; step_count?: number };
type Account = { id: string; provider: string; email: string; status: string };
type EventRow = { id: string; type: string; contact_id: string | null; created_at: string };

function ContactDetail({ contact, form, onChange, onClose, onSave, onDelete }: { contact: Contact; form: { firstName: string; lastName: string }; onChange: (patch: Partial<{ firstName: string; lastName: string }>) => void; onClose: () => void; onSave: () => void; onDelete: () => void }) {
  return (
    <div className="contact-detail">
      <div className="panel-head"><div><p className="eyebrow">Contact</p><h3>{contact.email}</h3></div><button className="text-button" onClick={onClose}>← Back</button></div>
      <div className="contact-form">
        <label>First name<input value={form.firstName} onChange={e => onChange({ firstName: e.target.value })} /></label>
        <label>Last name<input value={form.lastName} onChange={e => onChange({ lastName: e.target.value })} /></label>
        <div className="contact-actions">
          <button onClick={onSave}>Save changes</button>
          <button className="danger" onClick={onDelete}>Delete contact</button>
        </div>
      </div>
      <p className="table-note">Created {contact.created_at?.slice(0, 10)}</p>
    </div>
  );
}

function Dashboard() {
  const [notice, setNotice] = useState("Workspace ready");
  const [section, setSection] = useState("Overview");
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [events, setEvents] = useState<EventRow[]>([]);
  const [selectedContact, setSelectedContact] = useState<Contact | null>(null);
  const [editForm, setEditForm] = useState<{ firstName: string; lastName: string }>({ firstName: "", lastName: "" });
  const [searchQuery, setSearchQuery] = useState("");
  const [lists, setLists] = useState<Array<{ id: string; name: string; contact_count: number }>>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [listName, setListName] = useState("");
  const [targetList, setTargetList] = useState("");
  const [importReport, setImportReport] = useState<{ inserted: number; skipped: number; invalid: number } | null>(null);
  const [mockEmail, setMockEmail] = useState("");
  const [form, setForm] = useState<{ name: string; steps: Array<{ subject: string; body: string; delay: number }> }>({ name: "", steps: [{ subject: "", body: "", delay: 0 }] });
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadAll = async () => {
    const [c, k, a, e] = await Promise.all([api("/api/contacts"), api("/api/campaigns"), api("/api/sending-accounts"), api("/api/events")]);
    if (c.contacts) setContacts(c.contacts);
    if (k.campaigns) setCampaigns(k.campaigns);
    if (a.accounts) setAccounts(a.accounts);
    if (e.events) setEvents(e.events);
  };
  useEffect(() => { loadAll(); }, []);
  useEffect(() => { api("/api/contact-lists").then(result => { if (result.lists) setLists(result.lists); }); }, []);

  useEffect(() => {
    const term = searchQuery.trim();
    const fetchFiltered = async () => {
      const url = term ? `/api/contacts?q=${encodeURIComponent(term)}` : "/api/contacts";
      const result = await api(url);
      if (result.contacts) setContacts(result.contacts);
    };
    const handle = setTimeout(() => { fetchFiltered(); }, 250);
    return () => clearTimeout(handle);
  }, [searchQuery]);

  const selectContact = async (c: Contact) => {
    setSelectedContact(c);
    setEditForm({ firstName: c.first_name || "", lastName: c.last_name || "" });
  };
  const handleSaveContact = async () => {
    if (!selectedContact) return;
    const result = await api(`/api/contacts/${selectedContact.id}`, { method: "PATCH", body: JSON.stringify({ firstName: editForm.firstName, lastName: editForm.lastName }) });
    if (result.id) {
      setNotice("Contact updated");
      setSelectedContact(null);
      loadAll();
    } else {
      setNotice(result.error || "Unable to update contact");
    }
  };
  const handleDeleteContact = async () => {
    if (!selectedContact) return;
    if (!confirm("Delete this contact? This cannot be undone.")) return;
    const result = await api(`/api/contacts/${selectedContact.id}`, { method: "DELETE" });
    if (result.ok) {
      setNotice("Contact deleted");
      setSelectedContact(null);
      loadAll();
    } else {
      setNotice(result.error || "Unable to delete contact");
    }
  };
  const createList = async (e: React.FormEvent) => { e.preventDefault(); const result = await api("/api/contact-lists", { method: "POST", body: JSON.stringify({ name: listName }) }); if (result.id) { setLists(current => [...current, result]); setTargetList(result.id); setListName(""); setNotice(`List "${result.name}" created`); } else setNotice(result.error || "Unable to create list"); };
  const addToList = async () => { if (!targetList || !selectedIds.length) return; const result = await api(`/api/contact-lists/${targetList}/members`, { method: "POST", body: JSON.stringify({ contact_ids: selectedIds }) }); setNotice(`${result.added || 0} contacts added to the list`); setSelectedIds([]); api("/api/contact-lists").then(value => { if (value.lists) setLists(value.lists); }); };
  const importContacts = async (file: File) => {
    try {
      const data = new FormData(); data.append("file", file);
      const result = await api("/api/contacts/import", { method: "POST", body: data });
      if (result.inserted != null) { setImportReport(result); setNotice(`${result.inserted} imported · ${result.skipped} skipped · ${result.invalid} invalid`); }
      else setNotice(result.error || "No new contacts imported");
      const fresh = await api("/api/contacts");
      if (fresh.contacts) setContacts(fresh.contacts);
    } catch { setNotice("Contact import failed. Check the CSV and try again."); }
  };

  const handleContactsFile = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) await importContacts(file);
    event.target.value = "";
  };
  const createCampaign = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await api("/api/campaigns", { method: "POST", body: JSON.stringify({ name: form.name, steps: form.steps.map(st => ({ subject: st.subject, body: st.body, delay_minutes: st.delay })) }) });
    if (result.id) { setNotice(`Campaign "${result.name}" created as draft`); setForm({ name: "", steps: [{ subject: "", body: "", delay: 0 }] }); loadAll(); }
    else setNotice(result.error || "Unable to create campaign");
  };
  const updateStep = (index: number, patch: Partial<{ subject: string; body: string; delay: number }>) => setForm(f => ({ ...f, steps: f.steps.map((st, i) => i === index ? { ...st, ...patch } : st) }));
  const addStep = () => setForm(f => ({ ...f, steps: [...f.steps, { subject: "", body: "", delay: 0 }] }));
  const removeStep = (index: number) => setForm(f => f.steps.length > 1 ? { ...f, steps: f.steps.filter((_, i) => i !== index) } : f);
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
  const removeAccount = async (account: Account) => {
    if (!confirm(`Remove ${account.email}? This disconnects the account and cannot be undone.`)) return;
    const result = await api(`/api/sending-accounts/${account.id}`, { method: "DELETE" });
    if (result.ok) { setNotice(`${account.email} removed`); loadAll(); }
    else setNotice(result.error || "Unable to remove account");
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
              <button type="button" className="stat-link" onClick={() => setSection("Contacts")}><span>Contacts</span><strong>{contacts.length || "—"}</strong><small>{contacts.length ? "Manage your list ↗" : "awaiting first import"}</small></button>
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
          {importReport && <div className="import-report"><b>Last import</b><span>{importReport.inserted} imported</span><span>{importReport.skipped} skipped</span><span className={importReport.invalid ? "invalid" : ""}>{importReport.invalid} invalid rows</span></div>}
          {selectedContact ? <ContactDetail contact={selectedContact} form={editForm} onChange={patch => setEditForm(form => ({ ...form, ...patch }))} onClose={() => setSelectedContact(null)} onSave={handleSaveContact} onDelete={handleDeleteContact} /> : <>
            <input className="search-input" placeholder="Search contacts..." value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
            <div className="list-tools"><form onSubmit={createList}><input aria-label="New list name" placeholder="New list name" value={listName} onChange={e => setListName(e.target.value)} required /><button type="submit">Create list</button></form>{lists.length > 0 && <div className="list-assign"><select aria-label="Choose list" value={targetList} onChange={e => setTargetList(e.target.value)}><option value="">Choose a list</option>{lists.map(list => <option key={list.id} value={list.id}>{list.name} ({list.contact_count})</option>)}</select><button type="button" onClick={addToList} disabled={!targetList || !selectedIds.length}>Add {selectedIds.length || "selected"} to list</button></div>}</div>
            {contacts.length ? <div className="table">{contacts.slice(0, 50).map(c => <div className="row" key={c.id}><input type="checkbox" aria-label={`Select ${c.email}`} checked={selectedIds.includes(c.id)} onChange={e => setSelectedIds(ids => e.target.checked ? [...ids, c.id] : ids.filter(id => id !== c.id))} /><button type="button" className="row-contact" onClick={() => selectContact(c)}><b>{[c.first_name, c.last_name].filter(Boolean).join(" ") || "—"}</b><span>{c.email}</span></button></div>)}{contacts.length > 50 && <p className="table-note">Showing first 50 of {contacts.length}</p>}</div> : <div className="empty"><span>∿</span><b>No contacts yet</b><p>Import a CSV to get started.</p></div>}
          </>}
        </section>}

        {section === "Campaigns" && <section className="panel">
          <div className="panel-head"><div><p className="eyebrow">Sequences</p><h3>Campaigns ({campaigns.length})</h3></div></div>
          <form className="create-campaign" onSubmit={createCampaign}>
            <input aria-label="Campaign name" placeholder="Campaign name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required />
            {form.steps.map((st, i) => <fieldset className="step-row" key={i}>
              <legend>Step {i + 1}</legend>
              <input aria-label={`Step ${i + 1} subject`} placeholder={i === 0 ? "First email subject" : `Email ${i + 1} subject`} value={st.subject} onChange={e => updateStep(i, { subject: e.target.value })} required />
              <textarea aria-label={`Step ${i + 1} body`} placeholder={`Email ${i + 1} body`} value={st.body} onChange={e => setForm(f => ({ ...f, steps: f.steps.map((x, j) => j === i ? { ...x, body: e.target.value } : x) }))} required />
              <div className="step-meta">
                <label>Delay after previous step (minutes)<input type="number" min={0} aria-label={`Step ${i + 1} delay`} value={st.delay} onChange={e => updateStep(i, { delay: Math.max(0, Number(e.target.value) || 0) })} /></label>
                {form.steps.length > 1 && <button type="button" className="text-button" onClick={() => removeStep(i)}>Remove ✕</button>}
              </div>
            </fieldset>)}
            <button type="button" className="text-button" onClick={addStep}>+ Add step</button>
            <button type="submit">Create draft campaign</button>
          </form>
          {campaigns.length ? campaigns.map(camp => <div className="record" key={camp.id}><div><b>{camp.name}</b><small>{camp.status} · {camp.step_count ?? 1} step{(camp.step_count ?? 1) === 1 ? "" : "s"} · created {camp.created_at?.slice(0, 10)}</small></div>{camp.status === "draft" && <button className="text-button" onClick={() => approve(camp.id)}>Approve ✓</button>}{camp.status !== "draft" && <button className="text-button" onClick={() => enrollAll(camp)}>Enroll contacts</button>}</div>) : <div className="empty"><span>∿</span><b>No campaigns yet</b><p>Create your first sequence above.</p></div>}
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
          {accounts.length ? accounts.map(a => <div className="record" key={a.id}><div><b>{a.email}</b><small>{a.provider} · {a.status}</small></div><button className="text-button danger-text" type="button" onClick={() => removeAccount(a)}>Remove</button></div>) : <div className="empty"><span>∿</span><b>No sending accounts</b><p>Connect Gmail or Microsoft via OAuth, or add a mock account for testing. Credentials stay encrypted server-side.</p></div>}
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
