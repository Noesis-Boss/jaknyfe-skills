---
name: hook-generator
description: Generate an attention-grabbing first line of text for an auto-posted X post, article, or any other top-of-copy surface. Use when the user wants a strong opener — a hook — for a tweet, an article intro, a blog title, a video caption, a cold email subject, a LinkedIn post, or any writing where the first line decides whether the rest gets read. Triggers on phrases like "write a hook", "first line", "opener", "headline", "catchy intro", "give me a hook for", "make this tweet pop", "I need an attention grabber", or when an automation / agent is about to post to X or publish an article and needs the opening line written. Produces multiple hook variants in proven styles (curiosity, contrarian, stat, story, question, bold claim) with rationale and a recommendation.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Hook Generator

Write the first line. The first line is the whole game on X, the first paragraph of articles, the subject of cold emails. If it doesn't earn the second look, nothing else matters.

## What you produce

For every request, generate **5 hook variants** in different styles, each with a one-sentence rationale. End with a **recommended pick** and an optional **paired CTA / second line** if the surface allows it.

Output format (default):

```
HOOK 1 — [style: curiosity]
"<text>"
Why: <one sentence>

HOOK 2 — [style: contrarian]
"<text>"
Why: <one sentence>

HOOK 3 — [style: stat]
"<text>"
Why: <one sentence>

HOOK 4 — [style: story]
"<text>"
Why: <one sentence>

HOOK 5 — [style: bold claim]
"<text>"
Why: <one sentence>

RECOMMENDED: #N — <one line on why this one wins for the target surface>

SECOND LINE (optional): "<text that carries into the rest of the post>"
```

## Style toolkit

Pick from these — each one is a different psychological lever. Match the style to the surface and the audience, don't just rotate randomly.

- **Curiosity** — open a loop the reader wants closed. "I was wrong about X for three years." "The cheapest way to [desirable outcome] is also the slowest." Avoid clickbait; the gap between promise and payoff must be honest.
- **Contrarian** — take a position the herd disagrees with, and earn it. "Most [common advice] is wrong." Frame it as a specific, falsifiable claim, not just hot air.
- **Stat / Number** — anchor with a concrete, surprising, verifiable figure. Lead with the number, not the topic. "73% of [X] do [Y]. The other 27% are why [Z]." The number must be real or flagged as an estimate.
- **Story / Scene** — drop the reader mid-moment. "It was 2:14am when I noticed the dashboard had been green for six hours straight." Specific time, place, detail. Skip preamble.
- **Bold claim** — make a claim so strong it's either clearly right or clearly wrong. "Reading 50 papers a week made me worse at my job for a year." Commitment forces engagement.
- **Question** — ask something the reader is already asking themselves. "Why does [X] still work in 2026?" Best when the question is sharp and the answer is not obvious.
- **Confession / admission** — own a mistake or reversal. "I almost deleted this account three times." Vulnerability earns trust, especially on X where everything else is a flex.
- **Specific > generic** — "Austin, March 4th, 4:02pm" beats "the other day." The more specific, the more real. Always push the user toward specifics.

## Surface-specific guidance

Tone and length shift with where the hook will live.

### X / Twitter (auto-post, ≤280 chars total)
- One line, ideally under 90 characters so it survives a retweet with comment.
- Avoid hashtags in the hook — they weaken the punchline. Move them to the end or drop them.
- Don't start with "I" if a stronger opener exists; "I" is the weakest word in English for an opener.
- Pair the hook with a thread hook or a quote-tweet bait if appropriate.
- 1st-person + specificity + a small surprise is the highest-converting X pattern.

### Article / blog intro (first paragraph)
- 1–2 sentences, ~20–40 words.
- The hook must do ONE of: open a curiosity loop, make a claim, or set a scene. Do not do all three at once.
- End the hook on a point of tension that the next paragraph resolves.

### Cold email subject
- ≤8 words. Specific > clever.
- Avoid: "Quick question", "Following up", "Idea for [X]", "Hello from [Y]" — these are all spam-shaped.
- Prefer: a hyper-specific observation, a referral name, a question the recipient would actually ask.

### LinkedIn post
- LinkedIn rewards first-person, slightly self-deprecating, lesson-style openings. "I got fired from my first PM job because I couldn't read a room." Outrage or humble-brag both work; pure bragging rarely does.
- LinkedIn is the only surface where line breaks (a single line of text, then a blank line) are a deliberate format choice — use them in the body, not the hook itself.

### YouTube / video title
- Front-load the most searchable, most specific noun. Specificity > cleverness.
- Parenthetical clarifiers convert: "Why X (and what it means for Y)".

### Newsletter subject
- Lowercase, conversational, 4–7 words is the proven sweet spot. "the quietest signal in the market this week"

## Anti-patterns — never write these as the hook

- "In today's fast-paced world…" / "In an era of…" — death.
- "Let me tell you about…" — kill it.
- "Have you ever wondered…" — they have, move on.
- Starting with a question that ends with "??" or "?". One is fine, two is weak.
- Generic verbs in the first three words: "Here is", "This is", "In this post", "Let's talk about".
- Pure emojis as the first character. Emojis in the middle are fine; leading emojis scream bot.
- Quoting a famous person as the hook unless the quote directly contradicts the expected take.
- Starting with "Why" + [vague noun] + "is the key to" + [success]. Overused beyond rescue.

## Inputs the skill needs

If the user gives you a topic, post idea, or paste of the body, you have what you need. If you have only a vague brief, ask 1–3 short questions before generating:

- What's the surface? (X / article / subject / etc.)
- Who's the audience in one phrase? ("busy founders", "left-of-center X users", "iOS devs")
- What's the desired reaction? (curiosity, agreement, share, click, action)

If the user is in a hurry (auto-post pipeline, cron job), skip the questions and produce the 5 hooks from the topic alone — flag the assumptions in the rationale.

## How to use this skill

1. Read the topic / body the user provided.
2. Decide the surface (X, article, subject, etc.) — if unclear, default to X and label it.
3. Generate 5 hooks across 5 different styles from the toolkit.
4. Pick a recommendation with a one-line reason.
5. If the user is on a tight character budget, also include a character count for each hook.
6. Keep the output short — a hook is not an essay. Total response should fit on one screen.

## Examples

### Example 1: X hook for a post about cold email

Input: "I'm writing an X post about how most cold email advice is wrong."

Output:
```
HOOK 1 — [contrarian]
"Most cold email advice is written for people who've never sent one."
Why: names the gap between advice-givers and practitioners.

HOOK 2 — [confession]
"I sent 4,000 cold emails last year. Here's what the gurus won't tell you."
Why: real number + "won't tell you" creates a forbidden-knowledge angle.

HOOK 3 — [stat]
"Reply rate on 'personalized' cold emails: 1.2%. Reply rate on blunt ones I wrote at 2am: 7.4%."
Why: hard numbers, surprising inversion.

HOOK 4 — [curiosity]
"The cheapest cold email I ever sent took 11 minutes to write and earned $42k."
Why: curiosity loop + concrete payoff number.

HOOK 5 — [question]
"Why do 'quick question' emails outperform the ones I spent an hour on?"
Why: asks something the audience is already puzzled by.

RECOMMENDED: #2 — the specificity (4,000 emails) plus the forbidden-knowledge frame is the strongest pull for an X audience.

SECOND LINE: "The personalization industry is selling you a cure that makes the disease worse."
```

### Example 2: Article intro for a piece on AI in medicine

Input: "Write the intro for a long-form article about AI in radiology. The article argues that AI is better at finding tumors than the average radiologist but worse at explaining itself."

Output:
```
The AI found the tumor before the doctor did. It also couldn't tell the patient why.

That gap — between diagnosis and explanation — is the real story of AI in radiology, and it's not a story about machines replacing humans. It's a story about what happens when software gets very good at one thing and very bad at another, and the people caught in the middle are the ones with cancer.
```

### Example 3: Cold email subject line

Input: "Cold email to a CTO at a Series B fintech. Offering a 30-min chat about their observability stack."

Output:
- `your observability bill probably doubled last quarter` (specific, names the pain, no fluff)
- `saw your p99 from the rtt post — quick question` (referenced prior work, lowercased, conversational)
- `3 things your traces are telling you that pagerduty isn't` (value-first, curiosity)

RECOMMENDED: the first one — specific, names a real cost pain, no SaaS-shaped tells.

## Integration with automations

This skill is designed to be called from a bot/agent that auto-posts to X or publishes an article. The contract:

- **Input**: a topic string (and optionally a surface flag and a body excerpt).
- **Output**: the 5-hook block + recommendation, in plain text. Easy to parse the `RECOMMENDED: #N` line if a downstream automation wants just the winner.

If you're wiring this into a pipeline, recommended hook = the line beginning with `RECOMMENDED: #N` — extract the quoted text after that, strip the quotes, and you have the auto-posted opener.
