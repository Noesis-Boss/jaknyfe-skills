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
type Campaign = { id: string; name: string; status: string; campaign_type?: "newsletter" | "sequence"; preview_text?: string; template?: string; scheduled_at?: string | null; created_at: string; step_count?: number };
type Account = { id: string; provider: string; email: string; status: string };
type EventRow = { id: string; type: string; contact_id: string | null; created_at: string };

function CampaignAnalytics({ campaignId }: { campaignId: string }) {
  const [analytics, setAnalytics] = useState<Record<string, number> | null>(null);
  useEffect(() => { api(`/api/campaigns/${campaignId}/analytics`).then(result => { if (result.analytics) setAnalytics(result.analytics); }); }, [campaignId]);
  if (!analytics) return <small className="analytics">No activity yet</small>;
  const max = Math.max(...Object.values(analytics), 1);
  return <small className="analytics">{Object.entries(analytics).map(([type, count]) => <span className="stat" key={type} title={`${type}: ${count}`}><span className="bar"><span style={{ width: `${Math.round((count / max) * 100)}%` }} /></span>{type} {count}</span>) || "No activity yet"}</small>;
}

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
  const [importReport, setImportReport] = useState<{ inserted: number; skipped: number; invalid: number; invalid_rows?: Array<{ row: number; email: string; reason: string }>; invalid_csv?: string } | null>(null);
  const [importListMode, setImportListMode] = useState("none");
  const [importListId, setImportListId] = useState("");
  const [importNewListName, setImportNewListName] = useState("");
  const [importListColumn, setImportListColumn] = useState("");
  const [mockEmail, setMockEmail] = useState("");
  const [form, setForm] = useState<{ name: string; campaignType: "newsletter" | "sequence"; previewText: string; template: string; scheduledAt: string; steps: Array<{ subject: string; body: string; delay: number }> }>({ name: "", campaignType: "sequence", previewText: "", template: "plain", scheduledAt: "", steps: [{ subject: "", body: "", delay: 0 }] });
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
      const data = new FormData(); data.append("file", file); data.append("list_id", importListMode === "existing" ? importListId : ""); data.append("new_list_name", importListMode === "new" ? importNewListName : ""); data.append("list_column", importListMode === "column" ? importListColumn : "");
      const result = await api("/api/contacts/import", { method: "POST", body: data });
      if (result.inserted != null) { setImportReport(result); setNotice(`${result.inserted} imported · ${result.skipped} skipped · ${result.invalid} invalid`); api("/api/contact-lists").then(value => { if (value.lists) setLists(value.lists); }); }
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
    const result = await api("/api/campaigns", { method: "POST", body: JSON.stringify({ name: form.name, campaign_type: form.campaignType, preview_text: form.previewText, template: form.template, scheduled_at: form.scheduledAt || undefined, steps: form.steps.map(st => ({ subject: st.subject, body: st.body, delay_minutes: st.delay })) }) });
    if (result.id) { setNotice(`${form.campaignType === "newsletter" ? "Newsletter" : "Campaign"} "${result.name}" created as draft`); setForm({ name: "", campaignType: "sequence", previewText: "", template: "plain", scheduledAt: "", steps: [{ subject: "", body: "", delay: 0 }] }); loadAll(); }
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
  const schedule = async (camp: Campaign) => {
    const scheduledAt = camp.scheduled_at || new Date(Date.now() + 5 * 60 * 1000).toISOString();
    const result = await api(`/api/campaigns/${camp.id}/schedule`, { method: "POST", body: JSON.stringify({ scheduled_at: scheduledAt }) });
    if (result.scheduled_at) { setNotice(`${camp.name} scheduled · ${result.queued || 0} message${result.queued === 1 ? "" : "s"} queued`); loadAll(); }
    else setNotice(result.error || "Unable to schedule campaign");
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
          <div className="import-panel"><b>Import contacts</b><span>Choose how imported contacts join a list.</span><div className="import-options"><select aria-label="Import list mode" value={importListMode} onChange={e => setImportListMode(e.target.value)}><option value="none">No list assignment</option><option value="existing">Add to existing list</option><option value="new">Create a new list</option><option value="column">Use CSV list column</option></select>{importListMode === "existing" && <select aria-label="Import target list" value={importListId} onChange={e => setImportListId(e.target.value)}><option value="">Choose a list</option>{lists.map(list => <option key={list.id} value={list.id}>{list.name}</option>)}</select>}{importListMode === "new" && <input aria-label="Import new list name" placeholder="New list name" value={importNewListName} onChange={e => setImportNewListName(e.target.value)} />}{importListMode === "column" && <input aria-label="CSV list column" placeholder="CSV column name, e.g. list" value={importListColumn} onChange={e => setImportListColumn(e.target.value)} />}<button type="button" onClick={() => fileInputRef.current?.click()}>Choose CSV</button></div></div>
          {importReport && <div className="import-report"><b>Last import</b><span>{importReport.inserted} imported</span><span>{importReport.skipped} skipped</span><span className={importReport.invalid ? "invalid" : ""}>{importReport.invalid} invalid rows</span>{importReport.invalid_csv && <button type="button" className="text-button" onClick={() => { const url = URL.createObjectURL(new Blob([importReport.invalid_csv!], { type: "text/csv" })); const link = document.createElement("a"); link.href = url; link.download = "invalid-contacts.csv"; link.click(); URL.revokeObjectURL(url); }}>Download invalid rows</button>}</div>}
          {selectedContact ? <ContactDetail contact={selectedContact} form={editForm} onChange={patch => setEditForm(form => ({ ...form, ...patch }))} onClose={() => setSelectedContact(null)} onSave={handleSaveContact} onDelete={handleDeleteContact} /> : <>
            <input className="search-input" placeholder="Search contacts..." value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
            <div className="list-tools"><form onSubmit={createList}><input aria-label="New list name" placeholder="New list name" value={listName} onChange={e => setListName(e.target.value)} required /><button type="submit">Create list</button></form>{lists.length > 0 && <div className="list-assign"><select aria-label="Choose list" value={targetList} onChange={e => setTargetList(e.target.value)}><option value="">Choose a list</option>{lists.map(list => <option key={list.id} value={list.id}>{list.name} ({list.contact_count})</option>)}</select><button type="button" onClick={addToList} disabled={!targetList || !selectedIds.length}>Add {selectedIds.length || "selected"} to list</button></div>}</div>
            {contacts.length ? <div className="table">{contacts.slice(0, 50).map(c => <div className="row" key={c.id}><input type="checkbox" aria-label={`Select ${c.email}`} checked={selectedIds.includes(c.id)} onChange={e => setSelectedIds(ids => e.target.checked ? [...ids, c.id] : ids.filter(id => id !== c.id))} /><button type="button" className="row-contact" onClick={() => selectContact(c)}><b>{[c.first_name, c.last_name].filter(Boolean).join(" ") || "—"}</b><span>{c.email}</span></button></div>)}{contacts.length > 50 && <p className="table-note">Showing first 50 of {contacts.length}</p>}</div> : <div className="empty"><span>∿</span><b>No contacts yet</b><p>Import a CSV to get started.</p></div>}
          </>}
        </section>}

        {section === "Campaigns" && <section className="panel">
          <div className="panel-head"><div><p className="eyebrow">Unified campaigns</p><h3>Campaigns ({campaigns.length})</h3></div></div>
          <form className="create-campaign" onSubmit={createCampaign}>
            <input aria-label="Campaign name" placeholder="Campaign name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required />
            <select aria-label="Campaign type" value={form.campaignType} onChange={e => setForm({ ...form, campaignType: e.target.value as "newsletter" | "sequence" })}><option value="sequence">Sequence — timed outreach</option><option value="newsletter">Newsletter — one editorial send</option></select>
            {form.campaignType === "newsletter" && <><input aria-label="Preview text" placeholder="Preview text" value={form.previewText} onChange={e => setForm({ ...form, previewText: e.target.value })} /><select aria-label="Newsletter template" value={form.template} onChange={e => setForm({ ...form, template: e.target.value })}><option value="plain">Plain</option><option value="editorial">Editorial</option><option value="announcement">Announcement</option></select><label className="schedule-field">Schedule <input type="datetime-local" value={form.scheduledAt} onChange={e => setForm({ ...form, scheduledAt: e.target.value })} /></label></>}
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
          {campaigns.length ? campaigns.map(camp => <div className="record" key={camp.id}><div><b>{camp.name}</b><small>{camp.campaign_type === "newsletter" ? "newsletter" : "sequence"} · {camp.status} · {camp.step_count ?? 1} step{(camp.step_count ?? 1) === 1 ? "" : "s"} · created {camp.created_at?.slice(0, 10)}</small><CampaignAnalytics campaignId={camp.id} />{camp.scheduled_at && <small>Scheduled {new Date(camp.scheduled_at).toLocaleString()}</small>}</div>{camp.status === "draft" && <button className="text-button" onClick={() => approve(camp.id)}>Approve ✓</button>}{camp.status === "approved" && <button className="text-button" onClick={() => enrollAll(camp)}>Enroll contacts</button>}{camp.status === "approved" && camp.campaign_type === "newsletter" && <button className="text-button" onClick={() => schedule(camp)}>Schedule ↗</button>}</div>) : <div className="empty"><span>∿</span><b>No campaigns yet</b><p>Create your first campaign above.</p></div>}
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
  return <main className="dashboard-shell"><section className="workspace" style={{ maxWidth: 620, margin: "auto" }}><div className="panel" style={{ marginTop: "12vh" }}><p className="eyebrow orange">SaaS-Mailer</p><h1>Sign in to your workspace.</h1><button type="button" onClick={() => { window.location.href = "/api/auth/oidc/start"; }}>Sign in with Noesis</button><form onSubmit={submit}><input aria-label="Email" type="email" value={email} onChange={event => setEmail(event.target.value)} placeholder="you@example.com" required /><input aria-label="Password" type="password" value={password} onChange={event => setPassword(event.target.value)} placeholder="Password" required /><button type="submit">Sign in</button></form>{error && <p role="alert">{error}</p>}<a className="text-button auth-toggle" href="https://auth.noesisgroup.com/if/flow/noesis-self-signup/">Create a Noesis account</a></div></section></main>;
}

api("/api/auth/me").then(result => createRoot(document.getElementById("root")!).render(<React.StrictMode>{result.userId ? <Dashboard /> : <Login />}</React.StrictMode>));
