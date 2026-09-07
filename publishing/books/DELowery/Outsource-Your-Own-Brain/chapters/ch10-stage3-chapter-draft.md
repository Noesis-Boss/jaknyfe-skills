# Design for portability, not for lock-In

Marcus never saw the price hike coming. For two years, he ran his entire copywriting business through a polished AI writing platform. His prompts lived in their library, his drafts in their editor, his best-performing variations tagged in their analytics. When the platform emailed him about a new pricing tier — a 34% increase — he spent three days trying to move his work to a competitor before giving up. Everything was exportable as plain text, but the prompt chains, the categorization, the version history, the fine-tuned model preferences — all of it lived in a database format no other tool could read. He paid the increase.

Vendor lock-in isn't a new concept. What's new is how quietly it happens with AI tools. Unlike a CRM migration where the pain is obvious, AI lock-in creeps in through convenience. The tool saves your prompts, organizes your outputs, learns your preferences — and slowly becomes the only place your system exists. You're not paying for software anymore. You're paying ransom for your own workflow.

## Vendor lock-In as the new subscription trap

The modern AI subscription model has a hidden architecture. The front door is a generous free tier and a clean interface. The back door is a proprietary format, a closed ecosystem, and a switching cost that compounds monthly. Every prompt you write inside a platform that can't be exported as plain text is a brick in the wall between you and the exit.

Consider what happened to Brandi, a brand strategist who built a twelve-step research protocol inside a popular AI workspace. Each step was a prompt that fed its output into the next. The chain worked beautifully — for months. Then the platform changed its pricing model from per-seat to per-generation, and her monthly cost quadrupled. When she tried to rebuild the chain in a different tool, she discovered the prompts themselves were non-exportable. She could copy the text of the final output, but the intermediate steps — the actual prompts with their system instructions, variable placeholders, and response parsing — existed only in the platform's proprietary format.

The lesson isn't that platforms are evil. They're businesses, and businesses optimize for retention. The lesson is that *you* should optimize for portability. Lock-in isn't defined by what you can export at the end. It's defined by what you can pick up and move at any moment without losing fidelity.

A practical test: open your primary AI tool right now. Find the export button. What comes out? If the answer is "plain text, markdown, or JSON files that any other tool can read," you're in good shape. If the answer is "a proprietary backup file that only this platform can restore," you've built your house on rented land.

## Markdown and local files as portable substrate

The most resilient systems I've seen share one trait: they store their intelligence in formats that predate the tools that created them. Markdown files in a local folder. JSON configs in a git repository. Plain text prompts with variables in curly braces. These formats will outlive every AI platform currently in existence — not because they're technically superior, but because they're *substrate-agnostic*. A markdown file written in 2013 opens identically in 2024. A proprietary prompt format from a defunct AI startup opens as garbage.

Dana, a pricing consultant, built her entire client analysis system on this principle. Her prompt library lives as markdown files in a folder structure: `/prompts/discovery/`, `/prompts/analysis/`, `/prompts/recommendations/`. Each file contains the system prompt, the variable placeholders, and a brief note on intended output format. She uses three different AI tools depending on the task — one for initial research, one for deep analysis, one for final polish — because her system doesn't care which tool reads the prompt. The prompt is a text file. Any tool that accepts text can run it.

The architecture is simple enough that a screenshot would bore you:

```
~/brain/
  /prompts/
    discovery/
      01-client-intake.md
      02-market-mapping.md
    analysis/
      01-competitive-audit.md
      02-gap-analysis.md
  /outputs/
    2026-Q3/
      client-name/
        analysis.md
  /config/
    system-prompts.md
    variable-glossary.md
```

This folder lives on her laptop. It syncs to a private git repository. If any of her three AI tools disappeared tomorrow, she'd spend an afternoon pasting the same markdown files into whatever tool replaced them. Her system isn't tool-dependent. It's format-dependent, and she chose a format that doesn't_expire.

The commitment here is small. Write prompts as markdown files, not as entries in a platform's prompt library. Store outputs as local files, not as tabs in a platform's history. Use a folder structure that makes sense to you, not one a platform imposed. The friction this adds — copying a prompt from your file into a tool's input box instead of clicking a saved prompt — is seconds. The freedom it buys is total.

## The weekend migration test

Here's a thought experiment that separates architecture from habit. Imagine your primary AI tool shuts down on a Friday. Not a price increase, not a feature deprecation — a hard shutdown, servers offline, no warning. You have the weekend to rebuild your system. Monday morning, you need to be operational.

How long does it take?

If the answer is "a few hours, tops" — you're portable. Your prompts exist as files, your outputs are backed up, your system doesn't depend on any tool-specific feature. You grumble, you find a new tool, you paste your prompts, you're back.

If the answer is "I'd have to rebuild from scratch" — you're locked in. And the longer you wait, the worse it gets.

Mike, a leadership coach, ran this test on himself after a scare with his primary tool's API outage. He assumed he was portable because he kept his prompts in a notes app. Forty minutes in, he realized he was wrong. His prompts referenced platform-specific variables — things like `{{conversation_history}}` and `{{previous_output}}` — that worked inside the tool but meant nothing to a different one. His "system" was actually a set of interdependent fragments that only functioned inside one platform's execution environment.

He spent the weekend making two changes. First, he rewrote every prompt to use plain-text variable syntax — `<CLIENT_NAME>`, `<PREVIOUS_SECTION>`, `<RESEARCH_DATA>` — with a note in each file explaining what that variable should contain. Second, he created a `README.md` in his prompts folder that mapped the execution flow: which prompt ran first, which output fed into which next prompt, where human checkpoints sat in the chain. By Sunday night, his system was platform-agnostic. He could hand it to a stranger and they could run it in any tool that accepted text input.

The migration test has three checkpoints:

**Can you locate everything?** If your system is scattered across a platform's saved prompts, chat history, and buried settings, start there. Gather. Consolidate. One folder.

**Can a tool-agnostic reader understand it?** If your prompts contain platform-specific syntax, variables, or features, rewrite them in plain text. No tool should be required to read your instructions.

**Can you execute it in a new tool within a day?** If you can't, map the dependencies. What breaks? What's missing? Each dependency you remove is a brick removed from the wall.

Run the test once. Fix what it reveals. Run it again in six months. The weekend migration test isn't about paranoia — it's about ensuring your system's value lives in *your* files, not in a company's servers.

## Version-Controlled prompts

There's a quiet killer in prompt-based workspaces: prompt drift. You write a prompt, it produces great results, you tweak it, it gets better, you tweak it again — and suddenly it's producing different output than it did two weeks ago, and you can't figure out why because the change you made on a Wednesday afternoon is lost to time.

Version control fixes this. Not the enterprise kind — the simple kind. Every prompt file gets a history. Every change gets a message. When output degrades, you can see what changed and when.

Ron, a content writer, learned this the hard way. He had a prompt for generating article outlines that worked reliably for three months. Then he edited it — a small change, he thought — and the next five outlines came back structurally different. He couldn't recall what he'd changed, and the tool's built-in history was limited to the last ten versions with no decent diff view. He spent two hours reconstructing the original prompt from memory and old chat logs.

Now he keeps his prompts in a git repository. Every edit is a commit. Every commit has a message: `tightened intro instruction`, `added citation requirement`, `adjusted tone toward warmer`. When output shifts, he runs `git log` on the prompt file, scans the recent commits, and finds the change in seconds. When a change produces worse results, he reverts with `git checkout`. No reconstruction, no guesswork.

The implementation doesn't require deep git knowledge. Initialize a repository in your prompts folder. Before editing a prompt, stage and commit the current version with a one-line message. After editing, commit again. That's it. If you've never used git, the commands are `git init` (once), `git add .` (before committing), `git commit -m "your message"` (the commit), `git log` (see history), `git checkout <hash> -- filename.md` (restore a previous version).

The payoff compounds. After three months, you'll have a history of every prompt's evolution. You'll see which changes improved output and which didn't. You'll catch drift before it becomes degradation. And — critically for our portability theme — your prompts will exist as files in a repository that any tool, any platform, any future version of yourself can access.

This pairs with the weekend migration test naturally. A version-controlled prompt repository *is* a portable system. It's a folder of plain text files with a history. You can clone it to a new machine, paste its contents into any tool, and be operational in minutes. The version control doesn't add complexity to migration — it *is* the migration path.

There's a discipline here that matters: commit before you change, not after. The version you're about to edit is the known-good baseline. If your edit makes things worse, you need the baseline to revert to. Committing only after edits means your history starts at the *changed* version, and the original is already lost. Make it a habit: open the prompt, commit it as-is, then edit.

## The cost of ignoring portability

Lock-in compounds. Every month you stay in a locked system, the switching cost grows. Your prompts multiply, your history deepens, your familiarity with the tool's quirks becomes a kind of expertise that doesn't transfer. The best time to design for portability was the day you started. The second best time is today.

The solopreneurs who thrive in the AI era won't be the ones who picked the best tool. Tools change. They'll be the ones whose systems survived the tool changing. A system built on markdown files, local storage, and version control survives any platform's business decisions. A system built inside a platform survives only as long as the platform's incentives align with yours.

Design for the day the tool disappears. If your system works on that assumption, it works on every other day too.

---

The portability principle answers *where* your system lives. The next question is *who* touches it — and specifically, when your own hands should leave it entirely. Chapter 11 picks up that thread: when to stop supervising, when to let the system run unattended, and how to recognize the moment your oversight has stopped adding safety and started adding latency.