Eight stories, locked.

## Story 1: the check-Out counter

"I'm done," Priya said, sliding her laptop into her bag. "Two years of Notion pages, and I want out."

Marcus looked up from his spreadsheet. "Export everything?"

"CSV dump. Looks like alphabet soup." She dropped into the chair across from his desk. "They hold your knowledge base hostage the moment you stop paying."

Marcus had been through this. Three years ago, his CRM vanished overnight when the company pivoted to enterprise-only pricing. He'd rebuilt every client note from memory and电子邮件 scraps. The scar tissue still ached.

"Show me your system," he said.

She opened Notion. Databases nested in databases. Relations linking relations. A wiki nobody else could read.

"You built a cathedral on rented sand," he said. Not cruel—just naming it.

Over six weeks, they rebuilt it. Obsidian vault. Plain Markdown. Folders she understood. Links that traveled anywhere. She synced it to a private GitHub repo so even the structure was versioned.

The first weekend, she migrated a single project. Opened it on her phone, her old backup laptop, a library computer. It just read. Nothing asked her to log in. Nothing nags for renewal.

"I can leave anytime," she said, almost to herself.

"That's the point," Marcus said. "Portability isn't about leaving. It's about not being afraid to."

She smiled. "Best subscription I ever cancelled."

## Story 2: the weekend migration test

Paul's arms were crossed before Dana finished speaking.

"We have all our SOPs in that tool," he said. "Workflows, checklists, three years of process documentation."

"Okay," Dana said. "Let's run the test."

Paul hated the test. Dana had brought it up two weeks ago: *Pick one project. Time yourself migrating it from your current tool to any alternative. If it takes longer than a weekend, you're locked in.*

"It'll take an hour," he said.

Saturday morning. He opened his account and clicked export. What came back was a JSON blob, semantically correct, human-hostile. Every dependency lived in the tool's proprietary relation graph. His checklists referenced documents that referenced templates that referenced automations.

By Sunday night, he had moved twelve pages. Out of four hundred. His wrists ached. He hadn't slept properly.

Monday standup. Dana raised an eyebrow.

"Locked," he said.

"How locked?"

"Leaving is worse than staying. That's how locked."

She nodded slowly. "Now you know what you're actually paying for. It's not the tool. It's the hostage fee."

Paul spent the next month writing plain Markdown doppelgängers of every SOP. Ugly folders. No relations. But when he migrated one to a new app, it took forty minutes. He ran the test again. Sixty minutes total. He logged it in his journal.

"Subscribed," he wrote. "Not imprisoned."

## Story 3: the prompt he forgot

Two years of work in a .zip.

Raj downloaded it on a whim—some cloud tool's archive export—then forgot about it. When the company shuttered its consumer line, he barely noticed. He'd already migrated three months prior.

What he hadn't done was check the archive.

June. He needed a prompt he'd iterated on for an entire product launch. Thirty versions of it, each one tightening the voice, dodging the guardrails, fixing the JSON formatting. The tool had a version history panel, but when the service sunsetted, the panel went with it.

He unzipped the archive. Folders. JSON files. Nested objects. Prompts as strings inside a payload object.

He spent four hours reconstructing one prompt from fragments. It worked, but he couldn't prove it was the version that had performed best.

That night he opened VS Code and wrote his next prompt directly into a file: `prompts/2026-06-launch/v3.md`. Next iteration, `v4.md`. He committed each to a private Git repo with a one-line message: what changed and why.

When the next tool sunsetted—and they always sunsetted—he ran `git log` and saw every decision. Every branch. Every abandoned variant.

"The prompt isn't the output," he told his business partner. "The iteration history is the asset. That's what's worth saving."

His partner shrugged. Raj didn't argue. He had the receipts now.

## Story 4: the designer who could leave

Marta's portfolio lived in Figma. Clean frames, conditional components, polished prototypes. Clients loved it.

Her writing lived in a cloud docs tool. Three unfinished case studies, two proposals, and a pricing guide.

When the pricing tool quadrupled its tier, she barely flinched. "I'll handle it Monday."

Monday came. Tuesday went. By Thursday, she had exported the docs tool's content to Markdown, rebuilt the structure in Obsidian, and cross-linked it to her portfolio screenshots (which lived as flat PNGs in a folder she controlled).

"You seem calm," her husband said over dinner.

"I can leave," she said. "That's all it is."

Her writing tool had tried lock-in the right way—loyalty tiers, team features, an invite system that pulled collaborators into dependency. But she had kept the substrate portable. Every case study was a `.md` file synced to a Git repo. Every proposal had a plain-text twin.

"When I leave," she said, "nothing breaks. My clients don't notice. My drafts don't orphan. I just point at the new thing and keep going."

He nodded. "That sounds like a superpower."

"It's not a superpower," Marta said. "It's a habit. You build it once, then it runs itself."

## Story 5: the consultant's insurance policy

Three thousand dollars a year. billed@hercompany.com.

That was what stood between Erik and total operational continuity. When the AI writing assistant he'd used for eighteen months rolled out its "team" pricing—250% increase—he paid it. Not because it was worth it. Because he had woven it into every client deliverable pipeline.

His client reports were generated, refined, and finalized inside the tool. Export existed, but only as unstyled text. The structure lived in the app's database.

"You got robbed," his colleague Elena said over coffee.

"I got captured," Erik corrected.

He couldn't leave without losing eighteen months of templates. Each template was prompts chained to prompts chained to format rules chained to style guides. None of it was documented outside the tool.

It took him four months. Every weekend, he pulled one client deliverable out, rewrote the prompt chain as a Markdown file, saved it to a Git repo, and ran it through a different tool. The first migration was brutal. The twelfth was a Saturday afternoon.

The next time a subscription tripled, he let it lapse. Switched providers on a Monday morning. Clients never knew.

"I paid the new price," he told Elena, "for exactly one of my tools. The one I can't replace. The rest—I can swap any of them in an afternoon now."

"How long did that take to set up?"

"About the same time I would have spent being trapped. Maybe less."

## Story 6: the vault

"Where do we keep the house style?"

Two years into the agency, this was a real question. Loui had been through three writing tools. Each migration lost something. Style guide fragments scattered across docs, comments, changelogs, Slack messages.

He dug a hole. Not literally.

`agency/vault/style-guide.md`. One file. Git-tracked. Every rule he'd ever defended with a red pen, written down in plain prose.

Then he invited the team to add. Not in the writing tool, where comments disappeared when threads archived. In the vault. Commits and pull requests only. Every style change had a history, an author, a reason.

When the agency's writing tool raised prices and Loui decided to switch, the migration took one day. The style guide never moved. The templates were Markdown files. The prompts were versioned alongside the copy they generated.

"You spent real time on this?" his COO asked, scanning the Git log.

"Less time than the last migration cost us," Loui said. "And we never pay that cost again."

The COO leaned back. "So the vault isn't really about the files. It's about the option."

"Exactly," Loui said. "I don't need to switch providers tomorrow. I need to know that I can. Every tool we use has to pass that test now."

The COO pulled up the style guide on her phone. Read it in plain text. No app. No login.

"Okay," she said. "I get it now."

## Story 7: lock-In by another name

The pitch deck called it "ecosystem value."

Three years into the tool, Candace had 400 documents, 60 templates, 25 automation workflows—all nested in one platform. Prompts referenced other prompts by ID. Templates pulled variables from a system that only the platform understood. Every integration was a bridge back to itself.

"It's not lock-in," the sales rep said on the renewal call. "It's depth."

Candace had heard "depth" before. Twice. The first tool had gone under with forty thousand documents and no migration path. The second had pivoted to enterprise and left her tier frozen in amber.

She let the renewal expire.

Spent a weekend reconstructing one workflow from scratch in three different tools. Each one read the same Markdown prompt. Each one wrote to the same local file. Each one's output diffed cleanly against the previous.

On Monday morning, her assistant asked which tool she was using now.

"All of them," Candace said. "Whichever one's cheapest this month."

Her assistant blinked.

"The prompts are mine," Candace said. "The templates are mine. The input files are mine. The tool is interchangeable. I'm not."

She hadn't become anti-tool. She'd become substrate-aware. Plain files, version-controlled, structured so any tool could pick them up. The subscription was now a service she hired and fired on price, not on fear.

## Story 8: the migration that almost wasn't

Friday, 4 PM. The email landed: "We're sunsetting our SMB tier on December 1."

Three weeks.

Mark's entire client onboarding system lived in that tool. Questionnaires, intake forms, proposal templates, the AI-generated first drafts he reviewed. Every artifact existed only inside the platform.

He ran toward the export button. What came back was a JSON tree so deeply nested that parsing it took him two hours in Python. Three hours to write the script. Six hours to convert the parsed objects back into Markdown files he could actually read.

By Sunday night, he had 220 `.md` files in a folder. No structure. No relations. Just text.

He didn't sleep that weekend, and he barely slept the following two weeks. But by December 1, his onboarding system ran from Markdown files double-clicked in any text editor. The AI prompts were plain text in a `prompts/` folder. His proposal template was a single file with variables marked `{{client_name}}`.

The next tool he chose, he chose for price. Not because it was good, but because if it failed, he'd be失去 nothing but the subscription fee.

He told his business coach: "I thought portability was paranoid. Turns out it's just insurance I never have to apologize for."

His coach smiled. "What did it cost you?"

"Two weeks. Once."

"And lock-in?"

"Two weeks every time. Forever."