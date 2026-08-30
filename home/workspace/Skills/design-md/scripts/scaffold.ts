/**
 * Scaffold a new DESIGN.md from templates.
 * Usage:
 *   bun run scaffold.ts --name "My Project" > DESIGN.md
 *   bun run scaffold.ts --name "My Project" --minimal > DESIGN.md
 *   bun run scaffold.ts --template heritage > DESIGN.md
 */

interface ScaffoldOptions {
  name: string;
  description?: string;
  minimal?: boolean;
  template?: string;
}

function parseArgs(): ScaffoldOptions {
  const args = process.argv.slice(2);
  const opts: ScaffoldOptions = { name: "My Project" };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--name" || args[i] === "-n") opts.name = args[++i];
    else if (args[i] === "--description" || args[i] === "-d") opts.description = args[++i];
    else if (args[i] === "--minimal" || args[i] === "-m") opts.minimal = true;
    else if (args[i] === "--template" || args[i] === "-t") opts.template = args[++i];
    else if (args[i] === "--help" || args[i] === "-h") {
      console.log(`Usage:
  bun run scaffold.ts --name "My Project" > DESIGN.md
  bun run scaffold.ts --name "My Project" --minimal > DESIGN.md
  bun run scaffold.ts --name "My Project" --template heritage > DESIGN.md

Templates: heritage, minimal-modern, dark-tech, playful`);
      process.exit(0);
    }
  }

  return opts;
}

const TEMPLATES: Record<string, string> = {
  heritage: `---
version: alpha
name: ${"{{NAME}}"}
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  on-primary: "#FFFFFF"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  h2:
    fontFamily: Public Sans
    fontSize: 36px
    fontWeight: 600
    lineHeight: 1.2
  h3:
    fontFamily: Public Sans
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.25
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
rounded:
  sm: 4px
  md: 8px
  lg: 12px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 80px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: "12px 24px"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: "12px 24px"
    border: "1px solid {colors.secondary}"
  card:
    backgroundColor: "{colors.neutral}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
---

## Overview

Architectural Minimalism meets Journalistic Gravitas. The UI evokes a premium matte finish — a high-end broadsheet or contemporary gallery. Clean, confident, and permanent.

## Colors

The palette is rooted in high-contrast neutrals and a single, evocative accent color.

- **Primary (#1A1C1E):** Deep ink for headlines and core text. Maximum readability, sense of permanence.
- **Secondary (#6C7278):** Sophisticated slate for borders, captions, metadata.
- **Tertiary (#B8422E):** "Boston Clay" — the sole driver for interaction. Used exclusively for primary actions and critical highlights. Never decorative.
- **Neutral (#F7F5F2):** Warm limestone foundation, softer than pure white.

## Typography

The typography strategy leverages two distinct weights of **Public Sans** for narrative and **Space Grotesk** for technical data.

- **Headlines:** Public Sans Semi-Bold (600), establishing an institutional and trustworthy voice.
- **Body:** Public Sans Regular at 16px for contemporary professionalism and long-form readability.
- **Labels:** Space Grotesk, strictly uppercase with generous letter spacing, for timestamps, metadata, and technical data.

## Layout

Fluid grid with max-width 1200px on desktop. Strict 8px spacing scale with 4px half-step for micro-adjustments. Components grouped using containment principles with generous internal padding (24px).

## Elevation & Depth

Tonal layers rather than heavy shadows. Soft off-white base with pure white content cards. Subtle 1px hairline borders for separation. No drop shadows on cards — use border + subtle background shift for elevation.

## Shapes

Architectural sharpness. All interactive elements use minimal 4px corner radius. Cards use 8–12px. Never pill-shaped buttons. Never border-radius above 12px.

## Components

- **Primary buttons:** Boston Clay (#B8422E) background, white text, 12px horizontal padding, 4px radius.
- **Secondary buttons:** Transparent, deep ink border, same padding.
- **Cards:** Warm limestone (#F7F5F2) background, 12px radius, 24px padding, 1px slate border.

## Do's and Don'ts

- ✅ Use Boston Clay exclusively for interactive elements
- ✅ Maintain generous whitespace — never crowd elements
- ✅ Use 8px base spacing scale
- ✅ Keep typography hierarchy clean — h1 → h2 → h3 → body
- ❌ Never use pill-shaped buttons
- ❌ Never use border-radius above 12px
- ❌ Never use Boston Clay decoratively
- ❌ Never use heavy font weights (700+) for headlines
- ❌ Never introduce additional accent colors`,

  "minimal-modern": `---
version: alpha
name: ${"{{NAME}}"}
colors:
  primary: "#0066FF"
  secondary: "#6B7280"
  accent: "#0066FF"
  error: "#EF4444"
  success: "#10B981"
  neutral-50: "#F9FAFB"
  neutral-100: "#F3F4F6"
  neutral-200: "#E5E7EB"
  neutral-700: "#374151"
  neutral-900: "#111827"
  on-primary: "#FFFFFF"
typography:
  display:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  h1:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  h3:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.3
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
rounded:
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 80px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: "10px 20px"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: "10px 20px"
    border: "1px solid {colors.primary}"
  card:
    backgroundColor: "{colors.neutral-50}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    border: "1px solid {colors.neutral-200}"
  input:
    backgroundColor: "{colors.neutral-50}"
    textColor: "{colors.neutral-900}"
    rounded: "{rounded.md}"
    padding: "10px 14px"
    border: "1px solid {colors.neutral-200}"
---

## Overview

Clean, modern, and professional. Distilled to essentials with deliberate restraint. Trustworthy blue primary, generous whitespace, and crisp typography. Feels like a well-designed productivity tool.

## Colors

- **Primary (#0066FF):** Confident blue for actions, links, and brand moments. Never decorative.
- **Secondary (#6B7280):** Neutral gray for supporting text, borders, icons.
- **Neutral scale:** 50–900 for backgrounds, surfaces, text hierarchy.
- **Semantic:** Error (#EF4444), Success (#10B981).

## Typography

Inter for everything. Single font family with weight variation (400 body, 500 labels, 600–700 headlines). Clean, modern, highly readable.

## Layout

Max-width 1200px desktop content area. 8px base spacing scale. Generous section padding (80px vertical). Cards use 24px internal padding.

## Elevation & Depth

Flat with subtle hairline borders. Shadows only for overlays/modals (0 4px 12px rgba(0,0,0,0.08)). Depth conveyed through background layering rather than heavy shadows.

## Shapes

Rounded corners at 6–8px for interactive elements, 12–16px for cards. No pill shapes. Consistent across all surfaces.

## Components

- **Primary buttons:** Blue (#0066FF), white text, 8px radius, 10px/20px padding.
- **Secondary buttons:** Transparent, blue border, same sizing.
- **Cards:** Light gray (#F9FAFB), 12px radius, 24px padding, 1px border.
- **Inputs:** Light background, 8px radius, 1px border, focus ring on primary.

## Do's and Don'ts

- ✅ Use consistent 8px spacing scale
- ✅ Maintain max-width 1200px content area
- ✅ Use primary blue for CTAs and links only
- ✅ Keep typography hierarchy predictable
- ❌ Never use gradients as primary backgrounds
- ❌ Never exceed 16px border-radius
- ❌ Never use primary blue as decoration
- ❌ Never mix font families`,

  "dark-tech": `---
version: alpha
name: ${"{{NAME}}"}
colors:
  primary: "#00FF88"
  secondary: "#8B5CF6"
  accent: "#00FF88"
  error: "#FF4444"
  success: "#00FF88"
  neutral-900: "#0A0A0F"
  neutral-800: "#12121A"
  neutral-700: "#1A1A24"
  neutral-600: "#2A2A38"
  neutral-300: "#808090"
  neutral-200: "#A0A0B0"
  neutral-100: "#D0D0D8"
  neutral-50: "#F0F0F4"
  on-primary: "#0A0A0F"
typography:
  display:
    fontFamily: JetBrains Mono
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
  h1:
    fontFamily: JetBrains Mono
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: JetBrains Mono
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  h3:
    fontFamily: JetBrains Mono
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: IBM Plex Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: IBM Plex Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  code:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: IBM Plex Sans
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.02em
rounded:
  none: 0px
  sm: 2px
  md: 4px
  lg: 8px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 80px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
    padding: "10px 20px"
  card:
    backgroundColor: "{colors.neutral-800}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
    border: "1px solid {colors.neutral-600}"
---

## Overview

Terminal-native, high-contrast, cyber-precision. Dark backgrounds with neon green accents. Monospace headlines, sans-serif body. Feels like a developer tool built by developers who care about every pixel.

## Colors

- **Primary (#00FF88):** Neon green — CTA buttons, links, data highlights. High contrast against dark backgrounds.
- **Secondary (#8B5CF6):** Purple — secondary accents, hover states, code highlights.
- **Neutral scale:** Deep blacks (900–800) for backgrounds, grays (700–600) for surfaces/borders, lights for text hierarchy.
- **Semantic:** Error (#FF4444), Success (#00FF88).

## Typography

JetBrains Mono for headlines and code. IBM Plex Sans for body text. Monospace headlines create a technical, terminal-native feel while body in sans-serif maintains readability.

## Layout

Max-width 960px for content (narrower, more focused). 8px base spacing. Tight, efficient layouts with intentional negative space. Compact card padding (16px internal).

## Elevation & Depth

Dark-on-dark layering with subtle 1px borders and low-opacity glows. Elevation conveyed through background brightness (darker = further back). No conventional shadows — use border glow for modals.

## Shapes

Sharp corners (0–2px) for most elements. 4px for cards. No rounded buttons. Terminal aesthetic — precision over softness.

## Components

- **Primary buttons:** Neon green background, dark text, 2px radius. Sharp and deliberate.
- **Cards:** Dark surface (#12121A), 4px radius, 1px subtle border.
- **Inputs:** Dark background, 1px border, neon green focus ring.

## Do's and Don'ts

- ✅ Use neon green only for interactive elements
- ✅ Maintain high contrast — dark backgrounds, light text
- ✅ Keep corners sharp (0–4px max)
- ✅ JetBrains Mono for all code and headlines
- ❌ Never use white backgrounds
- ❌ Never use rounded corners above 4px
- ❌ Never use conventional drop shadows — use glow borders
- ❌ Never introduce warm colors (red/orange/yellow beyond error red)
- ❌ Never use serif fonts`,

  playful: `---
version: alpha
name: ${"{{NAME}}"}
colors:
  primary: "#FF6B6B"
  secondary: "#4ECDC4"
  accent: "#FFE66D"
  error: "#FF4444"
  success: "#2ECC71"
  neutral-50: "#FFFBF0"
  neutral-100: "#FFF5E0"
  neutral-200: "#FFE8C0"
  neutral-600: "#6B5B4F"
  neutral-800: "#3D3028"
  neutral-900: "#1A1510"
  on-primary: "#FFFFFF"
typography:
  display:
    fontFamily: Fredoka
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.05
  h1:
    fontFamily: Fredoka
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.15
  h2:
    fontFamily: Fredoka
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  h3:
    fontFamily: Fredoka
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.3
  body:
    fontFamily: Nunito
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Nunito
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: Nunito
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.4
rounded:
  sm: 8px
  md: 12px
  lg: 16px
  xl: 20px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 80px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.full}"
    padding: "12px 28px"
  card:
    backgroundColor: "{colors.neutral-100}"
    rounded: "{rounded.xl}"
    padding: "{spacing.lg}"
    border: "2px solid {colors.neutral-200}"
---

## Overview

Warm, friendly, and joyful. Soft pastels with a bold coral primary. Rounded everything. Feels like a creative tool or children's app — approachable, energetic, impossible to take too seriously.

## Colors

- **Primary (#FF6B6B):** Warm coral — buttons, links, brand moments. Full of energy.
- **Secondary (#4ECDC4):** Fresh teal — secondary actions, highlights, decorative accents.
- **Accent (#FFE66D):** Sunny yellow — badges, highlights, subtle backgrounds.
- **Neutral scale:** Warm cream tones (50–200) for backgrounds, warm browns (600–900) for text.

## Typography

Fredoka for headlines — rounded, friendly, approachable. Nunito for body — soft and readable. All rounded, humanist typefaces that feel warm.

## Layout

Max-width 1100px. 8px base spacing. Generous padding everywhere. Cards with soft borders. Playful asymmetry in hero sections.

## Elevation & Depth

Light, airy shadows with warm undertones. No sharp shadows. Elevation through subtle color shifts and soft 0 2px 8px rgba warmth. Cards float gently.

## Shapes

Rounded everything. 8–20px corner radius scale. Pill-shaped buttons. Soft, friendly, zero sharp edges.

## Components

- **Primary buttons:** Coral background, pill shape (full radius), generous padding.
- **Cards:** Cream background (#FFF5E0), 20px radius, 2px warm border, soft shadow.
- **Inputs:** Cream background, 12px radius, warm focus ring.

## Do's and Don'ts

- ✅ Use rounded corners everywhere (8px+)
- ✅ Pill-shaped buttons
- ✅ Warm, cream backgrounds — never pure white
- ✅ Playful, energetic color combinations
- ✅ Fredoka for headlines, Nunito for body
- ❌ Never use sharp corners (0px)
- ❌ Never use dark mode (warm = on brand)
- ❌ Never use cold blues or grays as primary tones
- ❌ Never use tight spacing — generous padding everywhere
- ❌ Never use formal/serious typography`,
};

function generateMinimal(name: string): string {
  return `---
version: alpha
name: ${name}
colors:
  primary: "#0066FF"
  secondary: "#6B7280"
  error: "#EF4444"
  success: "#10B981"
  neutral-50: "#F9FAFB"
  neutral-100: "#F3F4F6"
  neutral-200: "#E5E7EB"
  neutral-700: "#374151"
  neutral-900: "#111827"
  on-primary: "#FFFFFF"
typography:
  h1:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: 6px
  md: 8px
  lg: 12px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: "10px 20px"
  card:
    backgroundColor: "{colors.neutral-50}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    border: "1px solid {colors.neutral-200}"
---

## Overview

Clean, modern, professional. ${name} interface should feel trustworthy, fast, and polished.

## Colors

- **Primary (#0066FF):** Main brand color — CTAs, links, key UI elements.
- **Secondary (#6B7280):** Supporting text, icons, borders.
- **Error (#EF4444):** Destructive actions, error states.
- **Success (#10B981):** Confirmations, success states.

## Components

- **Primary buttons:** Blue background, white text, 8px radius.
- **Cards:** Light gray background, 12px radius, 1px border.

## Do's and Don'ts

- ✅ Keep spacing consistent (8px base)
- ✅ Use primary color for interactive elements only
- ✅ Maintain clear typographic hierarchy
- ❌ Never use gradients as primary backgrounds
- ❌ Never exceed 16px border-radius
- ❌ Never introduce additional accent colors
- ❌ Never use the primary color as decoration`;
}

function main() {
  const opts = parseArgs();

  if (opts.minimal) {
    process.stdout.write(generateMinimal(opts.name));
    return;
  }

  const template = TEMPLATES[opts.template || "minimal-modern"];
  if (!template) {
    console.error(`Unknown template: "${opts.template}". Available: ${Object.keys(TEMPLATES).join(", ")}`);
    process.exit(1);
  }

  const output = template.replace(/\{\{NAME\}\}/g, opts.name);
  process.stdout.write(output);
}

main();
