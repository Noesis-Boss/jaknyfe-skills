import { useState } from "react";

export default function App() {
  const [q, setQ] = useState("");
  const [reply, setReply] = useState("");
  const [busy, setBusy] = useState(false);
  const [joinStatus, setJoinStatus] = useState("");

  async function ask() {
    if (!q.trim()) return;
    setBusy(true);
    setReply("");
    try {
      const r = await fetch(`/api/ask?q=${encodeURIComponent(q)}`);
      const d = await r.json();
      setReply(d.reply ?? "");
    } catch {
      setReply("Concierge is offline right now.");
    } finally {
      setBusy(false);
    }
  }

  async function joinChannel() {
    const platform = (document.getElementById("platform") as HTMLSelectElement).value;
    const channelId = (document.getElementById("chanId") as HTMLInputElement).value;
    if (!channelId.trim()) { setJoinStatus("Enter a channel/group ID."); return; }
    const r = await fetch("/api/channels/join", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ platform, channelId, channelName: channelId }),
    });
    const d = await r.json();
    setJoinStatus(d.reply ?? "Join failed.");
  }

  return (
    <main className="wrap">
      <h1>🛎️ Concierge</h1>
      <p className="sub">Your trip companion · Phoenix ➜ Houston ➜ Cancún</p>
      <div className="box">
        <textarea
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask about flights, Cancún tips, packing, weather…"
        />
        <button onClick={ask} disabled={busy}>
          {busy ? "Thinking…" : "Ask Concierge"}
        </button>
      </div>
      {reply && <div className="reply">{reply}</div>}

      <details className="joinbox">
        <summary>Add Concierge to a group channel</summary>
        <p className="hint">Share this with the other 25 travelers — they can invite the bot to their Telegram / Slack / Discord group.</p>
        <div className="row">
          <select id="platform">
            <option value="telegram">Telegram</option>
            <option value="slack">Slack</option>
            <option value="discord">Discord</option>
          </select>
          <input id="chanId" placeholder="channel or group ID" />
          <button onClick={joinChannel}>Join</button>
        </div>
        {joinStatus && <div className="reply">{joinStatus}</div>}
      </details>

      <style>{`
        .wrap{max-width:640px;margin:8vh auto;font-family:system-ui,sans-serif;text-align:center;color:#0d1b2a}
        .sub{color:#52796f;margin-top:-6px}
        .box{display:flex;flex-direction:column;gap:10px;margin-top:24px}
        textarea{height:90px;border-radius:12px;border:1px solid #ccc;padding:12px;font-size:15px;resize:none}
        button{background:#1b4965;color:#fff;border:0;border-radius:12px;padding:12px;font-size:15px;cursor:pointer}
        button:disabled{opacity:.6}
        .reply{margin-top:20px;background:#eef4f6;border-radius:12px;padding:16px;text-align:left;white-space:pre-wrap}
        .joinbox{margin-top:28px;text-align:left;background:#f7fafb;border:1px solid #dde5e8;border-radius:12px;padding:12px 16px}
        .joinbox summary{cursor:pointer;font-weight:600;color:#1b4965}
        .hint{color:#52796f;font-size:13px}
        .row{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
        .row select,.row input{flex:1;min-width:120px;border-radius:10px;border:1px solid #ccc;padding:10px;font-size:14px}
      `}</style>
    </main>
  );
}

import { createRoot } from "react-dom/client";
createRoot(document.getElementById("root")!).render(<App />);
