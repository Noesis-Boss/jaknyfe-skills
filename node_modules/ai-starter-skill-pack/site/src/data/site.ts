export const REPO = 'https://github.com/Jeff-Kazzee/ai-starter-skill-pack';
export const SITE_URL = 'https://jeff-kazzee.github.io/ai-starter-skill-pack/';
export const INSTALL_CMD = 'npm install github:Jeff-Kazzee/ai-starter-skill-pack';
export const REVIEWED = '2026-06-23';

export const skillFile = (id: string) => `${REPO}/blob/HEAD/skills/${id}/SKILL.md`;

export interface Skill {
  id: string;
  name: string;
  tagline: string;
  use: string;
  get: string;
  example: string;
}

/** The five skills, in recommended order. */
export const skills: Skill[] = [
  {
    id: 'ai-beginner-onboarding',
    name: 'AI Beginner Onboarding',
    tagline: 'A calm place to start.',
    use: "you're overwhelmed and don't know where to begin with AI.",
    get: 'a tiny tool stack, a seven-day plan, one useful workflow, and one finishable practice project.',
    example:
      'I want to learn AI, but I only have a phone and ten minutes on low-energy days.',
  },
  {
    id: 'prompt-debugger',
    name: 'Prompt Debugger',
    tagline: 'Fix the prompt, not the symptom.',
    use: 'a prompt returns vague, generic, wrong, or badly formatted results.',
    get: 'a diagnosis of what actually broke, a rewritten prompt, model-specific variants, and test cases.',
    example:
      'Claude keeps ignoring the question after a long report. Diagnose the prompt.',
  },
  {
    id: 'personal-ai-tutor',
    name: 'Personal AI Tutor',
    tagline: 'Learn by doing, with proof.',
    use: 'you want a realistic learning path instead of an endless curriculum.',
    get: 'milestones, active practice, a proof artifact per milestone, and review checkpoints.',
    example:
      'Teach me to use coding agents without letting them write code I cannot explain.',
  },
  {
    id: 'ai-project-idea',
    name: 'AI Project Idea',
    tagline: 'Build something you can finish.',
    use: 'you want a small, realistic project worth building.',
    get: 'ranked ideas, one scoped MVP, a seven-day build plan, and a proof-of-work artifact.',
    example:
      'Give me a weird but useful AI project I can finish this weekend with public data.',
  },
  {
    id: 'no-bs-ai-career',
    name: 'No-BS AI Career',
    tagline: 'Turn learning into honest proof.',
    use: 'you want to connect AI learning to credible work — without overclaiming.',
    get: 'honest claims you can make now, a gap analysis, a portfolio plan, and a 30-day plan.',
    example:
      'What can I honestly put on my resume after building three personal AI demos?',
  },
];

export interface Question {
  text: string;
  skillId: string;
}

export const questions: Question[] = [
  { text: 'Where should I start?', skillId: 'ai-beginner-onboarding' },
  { text: 'Why did this prompt fail?', skillId: 'prompt-debugger' },
  { text: 'What should I learn next?', skillId: 'personal-ai-tutor' },
  { text: 'What can I build at my level?', skillId: 'ai-project-idea' },
  { text: 'How do I prove any of this?', skillId: 'no-bs-ai-career' },
];

export interface Runtime {
  name: string;
  note: string;
  path?: string;
}

export const runtimes: Runtime[] = [
  {
    name: 'Claude Code',
    note: 'Drop a skill folder into your project or personal skills directory.',
    path: '.claude/skills/  ·  ~/.claude/skills/',
  },
  {
    name: 'Codex',
    note: 'Place skills in the repository or user skills directory.',
    path: '.agents/skills/  ·  ~/.agents/skills/',
  },
  {
    name: 'OpenAI API',
    note: 'Upload versioned skill bundles for use with supported tool runtimes.',
  },
  {
    name: 'Zo Computer',
    note: 'Import via the Skills interface — it supports the standard Skill format.',
  },
  {
    name: 'ChatGPT & others',
    note: 'No generic folder loader. Paste a SKILL.md into project instructions as an approximation.',
  },
];

export interface Feature {
  title: string;
  body: string;
  icon: string;
}

export const features: Feature[] = [
  {
    title: 'When to trigger',
    body: 'A description tuned so the right skill activates from a natural question — and only then.',
    icon: 'target',
  },
  {
    title: 'When to stay out',
    body: 'Clear routing to the other skills, so onboarding does not try to do the tutor’s job.',
    icon: 'route',
  },
  {
    title: 'A real procedure',
    body: 'Step-by-step instructions, not a clever wording trick that only works once.',
    icon: 'list',
  },
  {
    title: 'Beginner-safe defaults',
    body: 'Privacy, pacing, and accessibility baked in — repeated inside each skill so it is safe alone.',
    icon: 'shield',
  },
  {
    title: 'A required output shape',
    body: 'A consistent, inspectable result instead of a wall of improvised text.',
    icon: 'layout',
  },
  {
    title: 'References & templates',
    body: 'Deeper methods and reusable worksheets the skill can pull in when needed.',
    icon: 'book',
  },
  {
    title: 'Trigger tests',
    body: 'Positive, negative, implicit, and boundary cases so a skill fires at the right time.',
    icon: 'check',
  },
  {
    title: 'No hidden cost',
    body: 'Instruction-only. No scripts, no paid API required, MIT-licensed, yours to fork.',
    icon: 'spark',
  },
];

export interface Stat {
  value: string;
  label: string;
}

/** Curated from docs/STATS.md — pack substance, not popularity metrics. */
export const stats: Stat[] = [
  { value: '5', label: 'Agent Skills' },
  { value: '25', label: 'Skill files' },
  { value: '8', label: 'Method references' },
  { value: '5', label: 'Trigger-eval suites' },
  { value: '$0', label: 'to get started' },
];

export interface DefaultItem {
  lead: string;
  rest: string;
}

export const defaults: DefaultItem[] = [
  {
    lead: 'One assistant you already have.',
    rest: 'No paid APIs, agents, or vector databases as a first step.',
  },
  {
    lead: '20–30 minutes a day,',
    rest: 'with a 10-minute low-energy option for hard days.',
  },
  {
    lead: 'Sample or redacted data first,',
    rest: 'before anything personal, client, school, or employer related.',
  },
  {
    lead: 'Model output kept separate',
    rest: 'from verified fact — assumptions are always labelled.',
  },
  {
    lead: 'One small finished artifact',
    rest: 'over a giant unfinished curriculum.',
  },
  {
    lead: 'Accessibility, fatigue, and budget',
    rest: 'treated as design constraints — not character flaws.',
  },
];
