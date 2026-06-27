import { useState } from "react";
import {
  Building2, Users, Target, Activity, DollarSign,
  ChevronRight, ChevronDown, Clock, CheckCircle2,
  Pause, Play, Briefcase, Code2, Megaphone, Plus,
  Shield, Cpu, GitBranch, Star, Timer, Layers,
  Sparkles, ArrowRight, AlertTriangle, LayoutDashboard,
  Eye
} from "lucide-react";

const T = {
  bg: "#09090f",
  s: "#111118",
  c: "#16161f",
  ch: "#1c1c28",
  b: "#252536",
  fg: "#eae6f2",
  m: "#706c82",
  ac: "#7c6aff",
  acd: "rgba(124,106,255,0.15)",
  acg: "rgba(124,106,255,0.25)",
  ok: "#00ddb5",
  wn: "#ffc048",
  er: "#ff5f6d",
  inf: "#5ca0ff",
  gd: "#ffc048",
  rs: "#f06595",
  tl: "#20c7a0"
};

const IC = {
  ceo: Star,
  cto: Code2,
  cmo: Megaphone,
  designer: Layers,
  engineer: Cpu,
  general: Briefcase,
  pm: Target,
  qa: Shield
};

const RC = {
  ceo: T.gd,
  cto: T.inf,
  cmo: T.wn,
  designer: T.rs,
  engineer: T.ok,
  general: T.m,
  pm: "#a29bfe",
  qa: T.tl
};

const RL = {
  ceo: "CEO",
  cto: "CTO",
  cmo: "CMO",
  designer: "Design",
  engineer: "Eng",
  general: "Agent",
  pm: "PM",
  qa: "QA"
};

const A = [
  { id: 1, name: "Hank Scorpio", role: "ceo", parent: null, status: "active", cost: 420, headcount: 0, success: 94, desc: "Strategic vision. Decides which industries to acquire next.", goals: 3, location: "Penthouse" },
  { id: 2, name: "Vera", role: "cto", parent: 1, status: "active", cost: 380, headcount: 12, success: 97, desc: "Massive laser operations. Decides which moons to de-mooon.", goals: 5, location: "R&D Lab" },
  { id: 3, name: "Homer Simpson", role: "cmo", parent: 1, status: "active", cost: 180, headcount: 6, success: 88, desc: "Brand presence. Decides what to do with the world's tallest pedestrian.", goals: 4, location: "Marketing Floor" },
  { id: 4, name: "Riley Tanner", role: "engineer", parent: 2, status: "active", cost: 120, headcount: 0, success: 96, desc: "Code generation, repo ops, CI/CD oversight.", goals: 8, location: "Eng Pod 3" },
  { id: 5, name: "Mira Volkov", role: "engineer", parent: 2, status: "active", cost: 120, headcount: 0, success: 91, desc: "Backend systems, infra, on-call rotation.", goals: 7, location: "Eng Pod 1" },
  { id: 6, name: "Joon Park", role: "designer", parent: 3, status: "active", cost: 95, headcount: 0, success: 93, desc: "UI/UX, brand assets, ad creative.", goals: 6, location: "Design Studio" },
  { id: 7, name: "Diego Marin", role: "pm", parent: 1, status: "active", cost: 85, headcount: 0, success: 89, desc: "Roadmap, sprint planning, stakeholder comms.", goals: 5, location: "PM Bullpen" },
  { id: 8, name: "Aisha Bekova", role: "qa", parent: 4, status: "active", cost: 75, headcount: 0, success: 99, desc: "Test automation, bug triage, regression suites.", goals: 4, location: "QA Wing" },
  { id: 9, name: "The Auditor", role: "general", parent: 2, status: "active", cost: 200, headcount: 0, success: 100, desc: "Compliance & risk. Reports directly to the board (Vera).", goals: 2, location: "Compliance" },
  { id: 10, name: "Lyle the Intern", role: "general", parent: 7, status: "paused", cost: 25, headcount: 0, success: 62, desc: "Misc tasks. Currently on coffee break.", goals: 1, location: "Mailroom" }
];

const G = [
  { id: 1, title: "Acquire the Denver Broncos", status: "in_progress", progress: 62, owner: "Hank Scorpio" },
  { id: 2, title: "Ship Laser R&D v3.2", status: "in_progress", progress: 84, owner: "Vera" },
  { id: 3, title: "Q3 Brand Refresh", status: "in_progress", progress: 41, owner: "Homer Simpson" },
  { id: 4, title: "Onboard 12 new paperclip factories", status: "in_progress", progress: 58, owner: "Diego Marin" },
  { id: 5, title: "Migrate infrastructure to TPU cluster", status: "in_progress", progress: 73, owner: "Mira Volkov" },
  { id: 6, title: "Audit Q2 compliance filings", status: "done", progress: 100, owner: "The Auditor" },
  { id: 7, title: "Re-brand 'Shelbyville' subsidiary", status: "in_progress", progress: 22, owner: "Joon Park" },
  { id: 8, title: "Reduce Lyle's coffee budget", status: "in_progress", progress: 5, owner: "Diego Marin" }
];

const E = [
  { ts: "12s ago", kind: "ok", agent: "Aisha Bekova", action: "passed 14/14 regression tests", detail: "QA-Pipeline-7" },
  { ts: "1m ago", kind: "ok", agent: "Riley Tanner", action: "merged PR #482 into main", detail: "paperclip-engine" },
  { ts: "3m ago", kind: "info", agent: "Hank Scorpio", action: "approved Q3 budget ($4.2M)", detail: "Boardroom" },
  { ts: "5m ago", kind: "ok", agent: "Vera", action: "deployed laser ops v3.2-rc1 to staging", detail: "infra-staging" },
  { ts: "8m ago", kind: "warn", agent: "Mira Volkov", action: "flagged memory pressure on TPU-3", detail: "Infra > Alerts" },
  { ts: "12m ago", kind: "info", agent: "Homer Simpson", action: "kicked off brand campaign brainstorm", detail: "Creative Room" },
  { ts: "18m ago", kind: "ok", agent: "The Auditor", action: "filed Q2 compliance report", detail: "Compliance" },
  { ts: "24m ago", kind: "ok", agent: "Diego Marin", action: "closed sprint 14 — 23/24 done", detail: "PM Bullpen" },
  { ts: "31m ago", kind: "warn", agent: "Joon Park", action: "requested feedback on Shelbyville re-brand", detail: "Design Studio" }
];

const KPIS = [
  { label: "Active Agents", val: "9", sub: "+1 vs last week", icon: Users, c: T.ac },
  { label: "Open Goals", val: "7", sub: "5 in progress, 2 done this week", icon: Target, c: T.wn },
  { label: "Monthly Burn", val: "$1.42M", sub: "+8% MoM", icon: DollarSign, c: T.rs },
  { label: "Throughput", val: "1,284", sub: "tasks completed (7d)", icon: Activity, c: T.ok }
];

const FIN = [
  { name: "Capital", total: 12_000_000, used: 7_400_000, delta: 1.2 },
  { name: "Operations", total: 4_500_000, used: 3_200_000, delta: -2.4 },
  { name: "R&D", total: 8_000_000, used: 4_100_000, delta: 0.8 },
  { name: "Marketing", total: 2_500_000, used: 1_750_000, delta: 4.1 }
];

function Bdg({ l, c }) {
  return <span style={{ background: c + "22", color: c, padding: "2px 8px", borderRadius: 999, fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.4 }}>{l}</span>;
}

function PBar({ p, c }) {
  return (
    <div style={{ width: "100%", height: 6, background: T.ch, borderRadius: 999, overflow: "hidden" }}>
      <div style={{ width: p + "%", height: "100%", background: c, borderRadius: 999 }} />
    </div>
  );
}

function Avatar({ role, size = 28 }) {
  const Icon = IC[role] || Briefcase;
  const c = RC[role] || T.m;
  return (
    <div style={{ width: size, height: size, borderRadius: size, background: c + "22", border: "1px solid " + c + "44", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
      <Icon size={Math.floor(size * 0.55)} style={{ color: c }} />
    </div>
  );
}

function Card({ children, style }) {
  return <div style={{ background: T.c, border: "1px solid " + T.b, borderRadius: 12, ...style }}>{children}</div>;
}

function Section({ icon: Icon, title, sub, right }) {
  return (
    <div style={{ padding: "14px 18px", borderBottom: "1px solid " + T.b, display: "flex", alignItems: "center", gap: 10 }}>
      {Icon && <Icon size={16} style={{ color: T.ac }} />}
      <div>
        <div style={{ fontWeight: 600, fontSize: 14 }}>{title}</div>
        {sub && <div style={{ fontSize: 12, color: T.m, marginTop: 2 }}>{sub}</div>}
      </div>
      {right && <div style={{ marginLeft: "auto" }}>{right}</div>}
    </div>
  );
}

function KPIGrid() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
      {KPIS.map((k, i) => {
        const Icon = k.icon;
        return (
          <Card key={i} style={{ padding: 16 }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
              <div style={{ width: 30, height: 30, borderRadius: 8, background: k.c + "22", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <Icon size={16} style={{ color: k.c }} />
              </div>
              <span style={{ fontSize: 10, color: T.m, textTransform: "uppercase", letterSpacing: 0.6 }}>{k.label}</span>
            </div>
            <div style={{ fontSize: 26, fontWeight: 700, letterSpacing: -0.5 }}>{k.val}</div>
            <div style={{ fontSize: 11, color: T.m, marginTop: 4 }}>{k.sub}</div>
          </Card>
        );
      })}
    </div>
  );
}

function AgentTree({ agents, selected, onSelect }) {
  const root = agents.find((a) => a.parent === null);
  const childrenOf = (id) => agents.filter((a) => a.parent === id);

  const render = (a, depth) => {
    const kids = childrenOf(a.id);
    const isSelected = selected === a.id;
    return (
      <div key={a.id}>
        <div
          onClick={() => onSelect(a.id)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "10px 14px",
            paddingLeft: 14 + depth * 18,
            cursor: "pointer",
            background: isSelected ? T.acd : "transparent",
            borderLeft: isSelected ? "2px solid " + T.ac : "2px solid transparent"
          }}
        >
          {kids.length > 0 ? <ChevronDown size={12} style={{ color: T.m }} /> : <div style={{ width: 12 }} />}
          <Avatar role={a.role} size={26} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span style={{ fontSize: 13, fontWeight: 600 }}>{a.name}</span>
              {a.status === "paused" && <Bdg l="paused" c={T.m} />}
            </div>
            <div style={{ fontSize: 11, color: T.m }}>{RL[a.role]} · {a.location}</div>
          </div>
          <div style={{ fontSize: 11, color: T.m, fontVariantNumeric: "tabular-nums" }}>${a.cost}k</div>
        </div>
        {kids.map((k) => render(k, depth + 1))}
      </div>
    );
  };

  return <div>{render(root, 0)}</div>;
}

function AgentDetail({ agent, agents }) {
  if (!agent) return null;
  const reports = agents.filter((a) => a.parent === agent.id);
  const c = RC[agent.role] || T.m;
  return (
    <div>
      <div style={{ padding: 20, display: "flex", alignItems: "center", gap: 14, borderBottom: "1px solid " + T.b }}>
        <Avatar role={agent.role} size={56} />
        <div style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <h2 style={{ fontSize: 20, fontWeight: 700, margin: 0 }}>{agent.name}</h2>
            <Bdg l={agent.status} c={agent.status === "active" ? T.ok : T.m} />
          </div>
          <div style={{ fontSize: 12, color: T.m, marginTop: 2 }}>{RL[agent.role]} · {agent.location}</div>
          <div style={{ fontSize: 13, marginTop: 8, color: T.fg, opacity: 0.9 }}>{agent.desc}</div>
        </div>
        <div style={{ display: "flex", gap: 6 }}>
          {agent.status === "paused" ? (
            <button style={{ background: T.ok, color: T.bg, border: 0, padding: "8px 12px", borderRadius: 8, cursor: "pointer", display: "flex", alignItems: "center", gap: 6, fontWeight: 600, fontSize: 12 }}>
              <Play size={12} /> Resume
            </button>
          ) : (
            <button style={{ background: T.c, color: T.fg, border: "1px solid " + T.b, padding: "8px 12px", borderRadius: 8, cursor: "pointer", display: "flex", alignItems: "center", gap: 6, fontSize: 12 }}>
              <Pause size={12} /> Pause
            </button>
          )}
          <button style={{ background: T.ac, color: T.bg, border: 0, padding: "8px 12px", borderRadius: 8, cursor: "pointer", display: "flex", alignItems: "center", gap: 6, fontWeight: 600, fontSize: 12 }}>
            <Plus size={12} /> Assign Goal
          </button>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", borderBottom: "1px solid " + T.b }}>
        {[
          { label: "Monthly Cost", val: "$" + agent.cost + "k", c: T.rs },
          { label: "Success Rate", val: agent.success + "%", c: T.ok },
          { label: "Reports", val: reports.length, c: T.inf },
          { label: "Active Goals", val: agent.goals, c: T.wn }
        ].map((s, i) => (
          <div key={i} style={{ padding: 14, borderRight: i < 3 ? "1px solid " + T.b : "none" }}>
            <div style={{ fontSize: 10, color: T.m, textTransform: "uppercase", letterSpacing: 0.6 }}>{s.label}</div>
            <div style={{ fontSize: 22, fontWeight: 700, marginTop: 4, color: s.c }}>{s.val}</div>
          </div>
        ))}
      </div>

      {reports.length > 0 && (
        <div style={{ padding: 18, borderBottom: "1px solid " + T.b }}>
          <div style={{ fontSize: 11, color: T.m, textTransform: "uppercase", letterSpacing: 0.6, marginBottom: 10, display: "flex", alignItems: "center", gap: 6 }}>
            <GitBranch size={12} /> Direct Reports ({reports.length})
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 8 }}>
            {reports.map((r) => (
              <div key={r.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: 10, background: T.ch, borderRadius: 8 }}>
                <Avatar role={r.role} size={24} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 12, fontWeight: 600 }}>{r.name}</div>
                  <div style={{ fontSize: 10, color: T.m }}>{RL[r.role]}</div>
                </div>
                {r.status === "paused" ? <Bdg l="paused" c={T.m} /> : <Bdg l="active" c={T.ok} />}
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ padding: 18 }}>
        <div style={{ fontSize: 11, color: T.m, textTransform: "uppercase", letterSpacing: 0.6, marginBottom: 10 }}>Performance (30d)</div>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 3, height: 60 }}>
          {Array.from({ length: 30 }).map((_, i) => {
            const h = 25 + Math.round(Math.sin(i * 0.7) * 18 + Math.random() * 12);
            return <div key={i} style={{ flex: 1, height: h, background: i === 29 ? c : c + "55", borderRadius: 2 }} />;
          })}
        </div>
      </div>
    </div>
  );
}

function GoalsView() {
  return (
    <Card>
      <Section icon={Target} title="Strategic Goals" sub="Quarterly objectives across the org" right={<button style={{ background: T.ac, color: T.bg, border: 0, padding: "6px 12px", borderRadius: 8, cursor: "pointer", display: "flex", alignItems: "center", gap: 6, fontSize: 12, fontWeight: 600 }}><Plus size={12} /> New Goal</button>} />
      <div>
        {G.map((g) => {
          const c = g.status === "done" ? T.ok : g.status === "in_progress" ? T.ac : T.m;
          return (
            <div key={g.id} style={{ padding: "12px 18px", borderBottom: "1px solid " + T.b + "66" }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 6 }}>
                <div>
                  <div style={{ fontWeight: 600, fontSize: 13 }}>{g.title}</div>
                  <div style={{ fontSize: 11, color: T.m, marginTop: 2 }}>Owner · {g.owner}</div>
                </div>
                <Bdg l={g.status.replace("_", " ")} c={c} />
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ flex: 1 }}><PBar p={g.progress} c={c} /></div>
                <div style={{ fontSize: 11, color: T.m, fontVariantNumeric: "tabular-nums", minWidth: 32, textAlign: "right" }}>{g.progress}%</div>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

function ActivityFeed() {
  const colorFor = (k) => (k === "ok" ? T.ok : k === "warn" ? T.wn : k === "err" ? T.er : T.inf);
  const iconFor = (k) => (k === "ok" ? CheckCircle2 : k === "warn" ? AlertTriangle : k === "err" ? AlertTriangle : Activity);
  return (
    <Card style={{ marginTop: 16 }}>
      <Section icon={Activity} title="Activity Feed" sub="Live org-wide events" right={<span style={{ display: "inline-flex", alignItems: "center", gap: 6, fontSize: 11, color: T.ok }}><span style={{ width: 6, height: 6, borderRadius: 6, background: T.ok, boxShadow: "0 0 8px " + T.ok }} /> Live</span>} />
      <div>
        {E.map((e, i) => {
          const Icon = iconFor(e.kind);
          const c = colorFor(e.kind);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 18px", borderBottom: i < E.length - 1 ? "1px solid " + T.b + "66" : "none" }}>
              <Icon size={14} style={{ color: c, flexShrink: 0 }} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <span style={{ fontSize: 12 }}>
                  <span style={{ fontWeight: 600 }}>{e.agent}</span> <span style={{ color: T.m }}>{e.action}</span>
                </span>
                <span style={{ fontSize: 11, color: T.m, marginLeft: 6 }}>— {e.detail}</span>
              </div>
              <span style={{ fontSize: 11, color: T.m, whiteSpace: "nowrap" }}>{e.ts}</span>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

function BudgetView() {
  return (
    <Card>
      <Section icon={DollarSign} title="Budget Allocation" sub="FY26 — $27M total" right={<Bdg l="Q3" c={T.wn} />} />
      <div style={{ padding: 18 }}>
        {FIN.map((b, i) => {
          const usedPct = (b.used / b.total) * 100;
          const c = usedPct > 75 ? T.er : usedPct > 50 ? T.wn : T.ok;
          return (
            <div key={i} style={{ marginBottom: 18 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 6 }}>
                <div>
                  <span style={{ fontSize: 13, fontWeight: 600 }}>{b.name}</span>
                  <span style={{ fontSize: 11, color: T.m, marginLeft: 10 }}>${(b.used / 1_000_000).toFixed(2)}M / ${(b.total / 1_000_000).toFixed(1)}M</span>
                </div>
                <div style={{ fontSize: 11, color: b.delta >= 0 ? T.ok : T.er, fontWeight: 600 }}>
                  {b.delta >= 0 ? "↑" : "↓"} {Math.abs(b.delta)}%
                </div>
              </div>
              <PBar p={usedPct} c={c} />
            </div>
          );
        })}
      </div>
    </Card>
  );
}

function Sidebar({ view, setView }) {
  const items = [
    { key: "dash", icon: LayoutDashboard, label: "Dashboard" },
    { key: "agents", icon: Users, label: "Agents" },
    { key: "goals", icon: Target, label: "Goals" },
    { key: "finance", icon: DollarSign, label: "Finance" }
  ];
  return (
    <div style={{ width: 220, background: T.s, borderRight: "1px solid " + T.b, display: "flex", flexDirection: "column" }}>
      <div style={{ padding: "18px 20px", borderBottom: "1px solid " + T.b, display: "flex", alignItems: "center", gap: 10 }}>
        <div style={{ width: 32, height: 32, borderRadius: 8, background: "linear-gradient(135deg, " + T.ac + ", " + T.rs + ")", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Building2 size={18} style={{ color: "#fff" }} />
        </div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 15, letterSpacing: -0.3 }}>Paperclip, Inc.</div>
          <div style={{ fontSize: 10, color: T.m }}>HAPPY HAPPENING HAPPY CO.</div>
        </div>
      </div>

      <nav style={{ flex: 1, padding: "10px 0" }}>
        {items.map((it) => {
          const Icon = it.icon;
          const isActive = view === it.key;
          return (
            <div
              key={it.key}
              onClick={() => setView(it.key)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "10px 20px",
                cursor: "pointer",
                background: isActive ? T.acd : "transparent",
                color: isActive ? T.ac : T.fg,
                fontSize: 13,
                fontWeight: isActive ? 600 : 500,
                borderLeft: isActive ? "2px solid " + T.ac : "2px solid transparent"
              }}
            >
              <Icon size={15} />
              {it.label}
            </div>
          );
        })}
      </nav>

      <div style={{ padding: 14, borderTop: "1px solid " + T.b }}>
        <div style={{ fontSize: 10, color: T.m, textTransform: "uppercase", letterSpacing: 0.6, marginBottom: 8 }}>System</div>
        {[
          { l: "All systems", c: T.ok, icon: CheckCircle2 },
          { l: "1 minor alert", c: T.wn, icon: AlertTriangle }
        ].map((s, i) => {
          const Icon = s.icon;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, padding: "4px 0", fontSize: 11, color: T.m }}>
              <Icon size={11} style={{ color: s.c }} /> {s.l}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function Topbar() {
  return (
    <div style={{ height: 56, background: T.s, borderBottom: "1px solid " + T.b, display: "flex", alignItems: "center", padding: "0 22px", gap: 16 }}>
      <div style={{ fontSize: 12, color: T.m, display: "flex", alignItems: "center", gap: 6 }}>
        <Building2 size={12} />
        Paperclip HQ
        <ChevronRight size={12} />
        <span style={{ color: T.fg, fontWeight: 500 }}>Operations</span>
      </div>
      <div style={{ flex: 1 }} />
      <div style={{ display: "flex", alignItems: "center", gap: 12, fontSize: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 6, color: T.m }}>
          <Clock size={12} /> 13:25 · America/Phoenix
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 6, color: T.ok }}>
          <span style={{ width: 6, height: 6, borderRadius: 6, background: T.ok }} /> 9 agents online
        </div>
        <div style={{ width: 28, height: 28, borderRadius: 14, background: T.ac + "33", border: "1px solid " + T.ac, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700 }}>
          D
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [view, setView] = useState("dash");
  const [selected, setSelected] = useState(1);

  return (
    <div style={{ display: "flex", height: "100vh", background: T.bg, color: T.fg, overflow: "hidden" }}>
      <Sidebar view={view} setView={setView} />
      <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
        <Topbar />
        <div style={{ flex: 1, overflow: "auto", padding: 22 }}>
          {view === "dash" && (
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 18 }}>
                <div>
                  <h1 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: -0.4 }}>Operations Dashboard</h1>
                  <div style={{ fontSize: 12, color: T.m, marginTop: 4 }}>Real-time view of the org — 9 agents, 7 open goals, $1.42M/mo burn</div>
                </div>
                <button style={{ background: T.ac, color: T.bg, border: 0, padding: "8px 14px", borderRadius: 8, cursor: "pointer", display: "flex", alignItems: "center", gap: 6, fontWeight: 600, fontSize: 12 }}>
                  <Sparkles size={12} /> Run Company Sync
                </button>
              </div>
              <KPIGrid />
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 16 }}>
                <GoalsView />
                <BudgetView />
              </div>
              <ActivityFeed />
            </div>
          )}

          {view === "agents" && (
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 18 }}>
                <div>
                  <h1 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: -0.4 }}>Agents</h1>
                  <div style={{ fontSize: 12, color: T.m, marginTop: 4 }}>Org chart & individual agent control</div>
                </div>
                <button style={{ background: T.ac, color: T.bg, border: 0, padding: "8px 14px", borderRadius: 8, cursor: "pointer", display: "flex", alignItems: "center", gap: 6, fontWeight: 600, fontSize: 12 }}>
                  <Plus size={12} /> Hire Agent
                </button>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "340px 1fr", gap: 16 }}>
                <Card>
                  <Section icon={Users} title="Organization" sub="Click an agent to inspect" />
                  <AgentTree agents={A} selected={selected} onSelect={setSelected} />
                </Card>
                <Card>
                  <AgentDetail agent={A.find((a) => a.id === selected)} agents={A} />
                </Card>
              </div>
            </div>
          )}

          {view === "goals" && (
            <div>
              <h1 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: -0.4, marginBottom: 4 }}>Goals</h1>
              <div style={{ fontSize: 12, color: T.m, marginBottom: 18 }}>Cross-org strategic objectives</div>
              <GoalsView />
            </div>
          )}

          {view === "finance" && (
            <div>
              <h1 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: -0.4, marginBottom: 4 }}>Finance</h1>
              <div style={{ fontSize: 12, color: T.m, marginBottom: 18 }}>FY26 budget allocation & burn rate</div>
              <BudgetView />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
