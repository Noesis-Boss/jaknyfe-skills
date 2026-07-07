import { useEffect, useState } from "react";

// Set after creating the Tier 1 Stripe product
const UPSELL_URL = "https://buy.stripe.com/8x24gzgNkexVa8h56mdMI04";

type Profile = {
  start_weight: number | null;
  target_weight: number | null;
  start_date: string | null;
};
type User = { id: number; email: string; provider: string };
type Entry = {
  date: string;
  weight: number | null;
  steps: number | null;
  calories_in: number | null;
  exercise_burn: number;
};

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [entries, setEntries] = useState<Entry[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");
  const [magicSent, setMagicSent] = useState(false);
  const [email, setEmail] = useState("");

  async function loadMe() {
    setLoading(true);
    const r = await fetch("/api/me");
    if (r.ok) {
      const d = await r.json();
      setUser(d.user);
      setProfile(d.profile);
      if (d.user) {
        const e = await fetch("/api/tracker");
        setEntries(e.ok ? (await e.json()).entries : []);
      }
    }
    setLoading(false);
  }
  useEffect(() => { loadMe(); }, []);

  if (loading) return <div className="app"><p className="sub">Loading…</p></div>;

  if (!user) return <Login onMagic={(m) => setMagicSent(m)} magicSent={magicSent} email={email} setEmail={setEmail} err={err} />;

  return (
    <div className="app">
      <div className="brand"><span className="dot" /><h1>The 50/50 Method</h1></div>
      <p className="sub">Walking + protein. Your brother's 100 lbs in 9 months system. {user.email}</p>

      {!profile?.target_weight && <ProfileSetup onDone={loadMe} />}

      <DailyEntry onDone={loadMe} />
      <Stats profile={profile} entries={entries} />
      <ProgressChart profile={profile} entries={entries} />
      <Upsell />
      <div className="btn-row">
        <button className="ghost" onClick={async () => { await fetch("/api/auth/logout", { method: "POST" }); setUser(null); }}>Log out</button>
      </div>
    </div>
  );
}

function Login({ onMagic, magicSent, email, setEmail, err }: any) {
  async function sendMagic() {
    const r = await fetch("/api/auth/magic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    const d = await r.json();
    if (r.ok) onMagic(true);
    else if (d.error === "email_not_configured") onMagic("resend");
    else onMagic(false);
  }
  return (
    <div className="app"><div className="center">
      <div className="brand" style={{ justifyContent: "center" }}><span className="dot" /><h1>The 50/50 Method</h1></div>
      <p className="sub">Track your walk + protein. Lose like the system that dropped 100 lbs in 9 months.</p>
      <div className="card">
        <a href="/api/auth/google"><button className="google-btn" style={{ width: "100%" }}>Continue with Google</button></a>
        <p className="note" style={{ textAlign: "center" }}>or</p>
        {magicSent === true && <p className="good note">Check your email for the sign-in link.</p>}
        {magicSent === false && <p className="err">Could not send. Try again.</p>}
        {magicSent === "resend" && <p className="err">Email sending not configured yet (Resend key missing). Use Google for now.</p>}
        <label>Email (magic link)</label>
        <input type="email" placeholder="you@email.com" value={email} onChange={(e) => setEmail(e.target.value)} />
        <button className="ghost" style={{ width: "100%" }} onClick={sendMagic}>Email me a sign-in link</button>
        {err && <p className="err">{err}</p>}
      </div>
      <p className="note">We store your entries so your progress carries across devices. No password needed.</p>
    </div></div>
  );
}

function ProfileSetup({ onDone }: any) {
  const [start, setStart] = useState("");
  const [target, setTarget] = useState("");
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));
  const [msg, setMsg] = useState("");
  async function save() {
    const r = await fetch("/api/profile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start_weight: Number(start), target_weight: Number(target), start_date: date }),
    });
    if (r.ok) { setMsg("saved"); onDone(); }
    else setMsg("error");
  }
  return (
    <div className="card">
      <h3>Set your baseline</h3>
      <div className="grid">
        <div><label>Start weight (lbs)</label><input type="number" value={start} onChange={(e) => setStart(e.target.value)} /></div>
        <div><label>Target weight (lbs)</label><input type="number" value={target} onChange={(e) => setTarget(e.target.value)} /></div>
        <div><label>Start date</label><input type="date" value={date} onChange={(e) => setDate(e.target.value)} /></div>
      </div>
      <button onClick={save}>Save baseline</button>
      {msg === "saved" && <p className="good note">Baseline saved.</p>}
    </div>
  );
}

function DailyEntry({ onDone }: any) {
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));
  const [weight, setWeight] = useState("");
  const [steps, setSteps] = useState("");
  const [cal, setCal] = useState("");
  const [burn, setBurn] = useState("");
  const [msg, setMsg] = useState("");
  async function save() {
    const r = await fetch("/api/tracker", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        date, weight: weight ? Number(weight) : null, steps: steps ? Number(steps) : null,
        calories_in: cal ? Number(cal) : null, exercise_burn: burn ? Number(burn) : 0,
      }),
    });
    if (r.ok) { setMsg("saved"); setWeight(""); setSteps(""); setCal(""); setBurn(""); onDone(); }
    else setMsg("error");
  }
  return (
    <div className="card">
      <h3>Log today</h3>
      <div className="grid">
        <div><label>Date</label><input type="date" value={date} onChange={(e) => setDate(e.target.value)} /></div>
        <div><label>Weight (lbs)</label><input type="number" value={weight} onChange={(e) => setWeight(e.target.value)} /></div>
        <div><label>Steps</label><input type="number" value={steps} onChange={(e) => setSteps(e.target.value)} /></div>
        <div><label>Calories eaten</label><input type="number" value={cal} onChange={(e) => setCal(e.target.value)} /></div>
        <div><label>Exercise burn</label><input type="number" value={burn} onChange={(e) => setBurn(e.target.value)} /></div>
      </div>
      <button onClick={save}>Save entry</button>
      {msg === "saved" && <p className="good note">Logged.</p>}
    </div>
  );
}

function Stats({ profile, entries }: { profile: Profile | null; entries: Entry[] }) {
  if (!profile?.target_weight) return null;
  const protein = Math.round(0.75 * profile.target_weight);
  const last = entries.filter((e) => e.calories_in != null).slice(-1)[0];
  const deficit = last ? 2000 + (last.exercise_burn || 0) - last.calories_in! : null;
  const stepsOk = entries.slice(-1)[0]?.steps ?? 0;
  const progress = profile.start_weight && profile.target_weight
    ? Math.max(0, Math.min(100, Math.round(((profile.start_weight - (last?.weight ?? profile.start_weight)) / (profile.start_weight - profile.target_weight)) * 100)))
    : 0;
  return (
    <div className="card">
      <h3>Today's targets</h3>
      <div className="grid">
        <div className="stat"><div className="label">Protein target</div><div className="value good">{protein} g</div></div>
        <div className="stat"><div className="label">Step target</div><div className={`value ${stepsOk >= 6000 ? "good" : "warn"}`}>{stepsOk >= 6000 ? "✓ 6k+" : (stepsOk || 0)}</div></div>
        <div className="stat"><div className="label">Deficit</div><div className={`value ${deficit != null ? (deficit >= 500 ? "good" : "bad") : "warn"}`}>{deficit != null ? `${deficit} cal` : "—"}</div></div>
        <div className="stat"><div className="label">Progress to goal</div><div className="value">{progress}%</div></div>
      </div>
    </div>
  );
}

function ProgressChart({ profile, entries }: { profile: Profile | null; entries: Entry[] }) {
  const weights = entries.filter((e) => e.weight != null).sort((a, b) => a.date.localeCompare(b.date));
  if (weights.length < 2 || !profile?.target_weight) return null;
  const w = 800, h = 220, pad = 30;
  const min = Math.min(...weights.map((e) => e.weight!), profile.target_weight) - 2;
  const max = Math.max(...weights.map((e) => e.weight!)) + 2;
  const xs = (i: number) => pad + (i * (w - 2 * pad)) / (weights.length - 1);
  const ys = (v: number) => h - pad - ((v - min) / (max - min)) * (h - 2 * pad);
  const line = weights.map((e, i) => `${xs(i)},${ys(e.weight!)}`).join(" ");
  const targetY = ys(profile.target_weight);
  return (
    <div className="card">
      <h3>Weight trend</h3>
      <svg viewBox={`0 0 ${w} ${h}`} style={{ width: "100%", height: "auto" }}>
        <line x1={pad} y1={targetY} x2={w - pad} y2={targetY} stroke="#16a34a" strokeDasharray="5 5" strokeWidth="1.5" />
        <text x={pad} y={targetY - 6} fill="#22c55e" fontSize="12">Target {profile.target_weight} lbs</text>
        <polyline points={line} fill="none" stroke="#f3f4f6" strokeWidth="2.5" />
      </svg>
    </div>
  );
}

function Upsell() {
  return (
    <div className="upsell">
      <h3>Want the full 12-week plan?</h3>
      <p>The free tracker is the front door. The Kickstart course lays out exactly how the 50 lbs in 3 months happened — walking protocol, protein math, deficit tightening, and the gym hand-off.</p>
      <a href={UPSELL_URL}><button>Unlock the 12-week plan →</button></a>
    </div>
  );
}
