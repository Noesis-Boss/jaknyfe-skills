# Memorization Science & Platform Brainstorm

> Research compiled 2026-08-03. Sources cited inline.

---

## Part 1: The Science — What Actually Works

### 1.1 The Cognitive Foundation

Three pillars govern durable memory formation:

**The Forgetting Curve (Ebbinghaus, 1885).** Without reinforcement, we lose ~50% of new information within an hour, ~70% within 24 hours, and ~90% within a week. Each recall resets and flattens the curve — this is why cramming fails and spacing wins.

**Encoding Specificity (Tulving & Thomson, 1973).** Memory retrieval is strongest when the context at recall matches the context at encoding. This is why actors who learn lines while moving/blocking remember them better on stage than actors who learned sitting at a desk.

**Dual Coding Theory (Paivio, 1971).** Information encoded through two channels — verbal + visual, or verbal + melodic — creates redundant retrieval paths. The melody-lyric binding in songs is the canonical example: when you recall the tune, the words tag along. [1]

### 1.2 The Evidence-Backed Techniques (Ranked)

| Rank | Technique | Effect Size | Best For |
|------|-----------|-------------|----------|
| 1 | **Active Recall** (testing yourself, not re-reading) | Largest effect across all memory research | Everything. Foundation layer. |
| 2 | **Spaced Repetition** (SM-2, FSRS algorithms — expanding intervals) | 2-3× retention vs. massed practice | Long-term retention of any discrete material |
| 3 | **Method of Loci / Memory Palace** | 2-3× recall improvement; neural changes visible on fMRI [2] | Ordered sequences, speeches, long chains |
| 4 | **Chunking + Progressive Disclosure** | Reduces cognitive load; increases working memory throughput | Long texts, scripts, ritual passages |
| 5 | **The Production Effect** (speaking aloud) | ~15-20% memory boost vs. silent reading [3] | Scripts, speeches, ritual |
| 6 | **First-Letter / Acronym Method** | Fast initial encoding; used by Robert Downey Jr. | Scripts, bullet-point sequences |
| 7 | **Melodic + Rhythmic Scaffolding** | Dual encoding; recall durability significantly higher [4] | Songs, ritual, poetry, anything set to meter |
| 8 | **Embodied / Kinesthetic Encoding** | Real-object engagement > picture-based [5] | Ritual with floor work, staged performances |
| 9 | **Sleep Consolidation** | Review before sleep; memory consolidates during slow-wave sleep | Everything. Underused. |

### 1.3 How These Stack for Different Use Cases

#### Acting Scripts
- **Chunking** into beats/units (where topic, emotion, or character shifts)
- **Cue-based recall**: learning your lines in relation to the OTHER character's last word — the "cue word" method that apps like coldRead and LineLearner automate
- **First-letter method**: write the first letter of each word on a page, use as a minimal prompt
- **Embodied practice**: run lines while doing physical tasks (vacuuming, walking) — builds context-independent recall [6]
- **Recall Rehearsal**: recite in reverse order to strengthen every link, not just forward chains

#### Masonic / Ritual Text
- Same challenges as acting scripts plus: archaic language, fixed exact wording, performance under pressure, floor work choreography
- **Memory palace** maps naturally onto lodge floor layouts — each station/ officer position becomes a locus
- Masonic tradition already uses acronym mnemonics (e.g., "TTGOTGAOTU") — this can be formalized
- Degree lectures are modular: learn as nested chunks (paragraph → sentence → phrase)
- **Progressive disclosure**: start with full text → hide every 5th word → hide every 3rd → first letter only → blank recall [7]

#### Songs / Lyrics
- **Melody-lyric binding**: the brain encodes lyrics and melody as one unit via the left inferior frontal gyrus and bilateral middle temporal gyrus [8]
- Rhythm provides a predictable scaffold: it constrains syllable count and word length, reducing the search space during recall
- **Spaced repetition with audio**: hearing the full track plus practicing with instrumental-only backing tracks
- Rhyme and alliteration in lyrics are themselves mnemonic devices

#### Long Lectures / Speeches
- **Memory palace** is the gold standard — Cicero and Quintilian used it for hours-long orations
- **Structural outline as skeleton**: memorize the 5-7 key transitions first, then fill in supporting points
- **Spaced repetition** of key statistics, quotes, and transitions

### 1.4 Algorithm Deep-Dive

**SM-2 (SuperMemo 2, 1987):** The foundational spaced-repetition algorithm. After each review, you rate recall quality (0-5). The algorithm adjusts an "easiness factor" (EF) per item:

```
EF' = EF + (0.1 - (5 - q) × (0.08 + (5 - q) × 0.02))
Next interval = previous interval × EF
```

Default schedule: 1 day → 6 days → 15 days → 37 days → 92 days (at EF=2.5). Cards you struggle with stay short; easy cards drift to months. [9]

**FSRS (Free Spaced Repetition Scheduler, 2023):** Replaces SM-2 in Anki. Uses machine learning to model memory as a function of stability and retrievability. Benchmarks on 500M+ reviews show FSRS needs 20-30% fewer reviews for the same retention rate. [10]

**Cloze Deletion:** Not an algorithm but a card format. "The Grand Lodge of Arizona was chartered in …[year]." You fill the blank. Cloze deletions are the fastest way to convert dense text into testable chunks. SuperMemo's incremental reading combines cloze with spaced repetition for book-length material. [11]

### 1.5 Existing Tools Landscape — What's Missing

| Tool | Strength | Gap |
|------|----------|-----|
| **Anki** | Best SRS engine (FSRS), open source | Card-based. No concept of "passage flow." Awkward for long texts. |
| **Memorize By Heart** | Purpose-built for text; progressive letter/word removal | Single-passage focus. No spaced repetition across passages. No multi-modal. |
| **LineLearner / coldRead / Rehearsal Pro** | Actor-specific: cue detection, scene partner simulation | Script-only. No ritual/song/lecture support. No spaced repetition. |
| **Script Rehearser** | Recording + gap playback for lines | Limited to dialogue format. No memory palace or progressive disclosure. |
| **Actameleon / Linerunner-t3** (OSS) | Structured script navigation, TTS, hide/reveal | Niche (theatre only). No spaced repetition engine. |
| **Obsidian Teleprompter Plus** | Markdown-based, auto-scroll, TTS | Teleprompter, not memorization trainer. No progressive difficulty escalation. |
| **Quizlet** | Flexible, spaced repetition | Flashcard paradigm. Bad for long sequential passages. |

**The gap:** No single tool combines (1) an SRS engine, (2) progressive disclosure for long sequential text, (3) multi-modal encoding (audio, visual, kinesthetic), and (4) domain-flexible passage types (scripts, ritual, songs, lectures). Existing tools are either SRS flashcards for facts OR script cue-players for actors — nothing bridges both.

---

## Part 2: Platform Brainstorm — "Mneme"

### 2.1 Core Concept

**Mneme** (Greek muse of memory) is a progressive-disclosure memorization engine for long-form sequential text. It treats a passage — whether a 3-minute Masonic lecture, a 10-page script scene, song lyrics, or a TED talk — as a single learnable object with internal structure, and applies spaced repetition, multi-modal encoding, and progressive difficulty escalation to move it from short-term to durable long-term memory.

### 2.2 What Makes It Different

1. **Passage-native, not card-native.** Anki forces you to atomize everything into Q&A pairs. Mneme keeps the passage whole and progressively obscures parts of it.

2. **Progressive difficulty ladder.** Each passage has a clear skill tree: Full Text → Word Removal (10%) → Word Removal (30%) → First Letter Only → Blank Recall → Cued Recall (hear the line before yours) → Cold Recall (no prompts). You don't advance until you demonstrate mastery at the current level.

3. **Spaced repetition at the passage level.** Each passage is an SRS item with its own interval and ease factor. When a passage comes due for review, you practice at your current difficulty level. The system tracks per-passage and per-segment performance.

4. **Domain-aware modes.** The same engine, different UX:
   - **Script Mode:** Cue-line detection, character assignment, scene partner TTS
   - **Ritual Mode:** Floor-work integration (lodge/officer position diagrams), archaic language glosses, exact-wording validation
   - **Song Mode:** Synced audio + lyrics, instrumental-only backing track generation, melody-line hum detection
   - **Lecture Mode:** Structural outline view, key-statistic highlighting, timing feedback

5. **Multi-modal encoding engine.** Per passage, you can attach: audio recording (you or TTS), visual memory palace map, kinesthetic notes ("walk the floor while reciting"), and first-letter cue sheets — all generated automatically.

### 2.3 Technical Architecture

```
┌─────────────────────────────────────────────────┐
│                  Mneme Core                       │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Passage   │  │ SRS       │  │ Progress      │  │
│  │ Engine    │  │ Engine    │  │ Engine         │  │
│  │           │  │ (FSRS)    │  │                │  │
│  │ - parse   │  │ - schedule│  │ - difficulty   │  │
│  │ - chunk   │  │ - adapt   │  │   ladder       │  │
│  │ - segment │  │ - track   │  │ - mastery gates│  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Audio     │  │ Visual    │  │ Export         │  │
│  │ Engine    │  │ Engine    │  │ Engine          │  │
│  │           │  │           │  │                │  │
│  │ - TTS     │  │ - palace  │  │ - cue sheets   │  │
│  │ - record  │  │   builder │  │ - PDF scripts  │  │
│  │ - backing │  │ - reveal  │  │ - audio files  │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │            Mode Plugins                    │    │
│  │  Script │ Ritual │ Song │ Lecture │ Custom │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

**Stack recommendation:**
- **Frontend:** React + TypeScript (or Next.js for SSR), Tailwind CSS, shadcn/ui
- **Backend:** Bun + Hono API (matches your existing stack)
- **Database:** SQLite via Drizzle ORM (single-file, zero-config, sufficient for single-user)
- **SRS Engine:** Custom FSRS implementation (the algorithm is well-documented, ~200 lines of TypeScript)
- **Audio:** Web Speech API for TTS (free, local) + optional ElevenLabs for quality
- **Auth:** None initially (local-first); add later if needed

### 2.4 Core Feature Set — v1 MVP

**Passage Management**
- Import: paste text, upload .txt/.pdf/.docx, or URL fetch
- Auto-chunking: detects natural breaks (paragraphs, scene headings, verse lines, stanza breaks)
- Manual re-chunking: drag to adjust segment boundaries
- Tags: "ritual", "EA Degree", "script", "song", "lecture"

**Practice Modes (Progressive Ladder)**
1. **Read-Through** — Full text displayed. You read aloud. System records timing baseline.
2. **Fade 10%** — Random 10% of words replaced with blanks (weighted toward content words, not function words)
3. **Fade 30%** — 30% blanks
4. **First Letter Only** — Shows `T_g_ w_s t_e n_g_t b_f_r_ C_r_s_m_s...` — you reconstruct
5. **Line Cue** — Shows the line before yours (for dialogue) or the section heading
6. **Cold Recall** — Nothing. You recite. Speech-to-text transcribes. System highlights errors.

**SRS Integration**
- Each passage is an SRS card. After practice, rate: "Forgot" (reset), "Hard" (interval × 1.2), "Good" (interval × EF), "Easy" (interval × EF × 1.3)
- Due passages appear in a daily queue
- Streak tracking and calendar heatmap

**Audio Tools**
- TTS playback of your lines (with gaps for you to fill)
- Voice recording: record yourself reciting, compare to reference
- "Scene partner" mode: plays other characters' lines, waits for yours
- Speed control (0.5× – 2×)

**Memory Palace Builder**
- Upload a floor plan or room photo
- Place numbered markers at key locations
- Assign passage segments to markers
- Practice mode: navigate palace visually while reciting

### 2.5 v2 Features (Post-Validation)

- **Collaboration:** Share passages. Lodge members can all practice the same ritual and see each other's progress (opt-in).
- **AI Passage Analysis:** LLM identifies key transitions, suggests chunk boundaries, generates memory palace anchor images, identifies archaic terms
- **Melody Line Detection:** For song mode — hum or sing the melody and the system verifies pitch contour against reference
- **Mobile app:** PWA first, native later.
- **Wearable mode:** Apple Watch / Wear OS — buzz your wrist with the cue word, practice hands-free
- **Offline-first sync:** Local DB with optional cloud sync via your Zo server

### 2.6 Why This Works for Ritual Specifically

Masonic/DeMolay ritual has unique demands:
1. **Exact wording** — paraphrasing isn't acceptable
2. **Floor work** — movement is choreographed to text
3. **Archaic language** — harder to encode than conversational English
4. **Performance pressure** — delivered in front of officers and candidates
5. **Modular structure** — degree lectures are delivered by different officers; each has their section

Mneme addresses each:
1. Exact wording → progressive disclosure with speech-to-text verification
2. Floor work → memory palace mapped to physical lodge layout; kinesthetic notes per passage
3. Archaic language → built-in glosses and etymology notes surfaced during practice
4. Performance pressure → cold recall mode simulates performance conditions
5. Modular structure → passage grouping by degree/office, per-officer progress tracking

### 2.7 Competitive Positioning

| Feature | Anki | Memorize By Heart | LineLearner | Script Rehearser | Mneme |
|---------|------|-------------------|-------------|------------------|-------|
| SRS Engine (FSRS) | ✅ | ❌ | ❌ | ❌ | ✅ |
| Progressive text disclosure | ❌ | ✅ | ❌ | ❌ | ✅ |
| Script cue detection | ❌ | ❌ | ✅ | ✅ | ✅ |
| Memory palace builder | ❌ | ❌ | ❌ | ❌ | ✅ |
| Song/lyric mode | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ritual mode | ❌ | ❌ | ❌ | ❌ | ✅ |
| Speech-to-text verification | ❌ | ❌ | ❌ | ❌ | ✅ |
| Domain-flexible | ❌ | Partial | ❌ | ❌ | ✅ |
| Open source | ✅ | ❌ | ❌ | ❌ | ✅ |

### 2.8 Development Path

**Phase 1: Core Engine (2-3 weeks)**
- Passage parser + chunker
- FSRS scheduler
- SQLite schema
- Basic CLI for testing

**Phase 2: Practice UI (3-4 weeks)**
- Progressive disclosure renderer
- Web-based practice interface
- TTS integration
- Difficulty ladder logic

**Phase 3: Domain Modes (2-3 weeks)**
- Script mode (cue detection)
- Song mode (synced lyrics + audio)
- Ritual mode (floor plan overlay)
- Lecture mode (outline view)

**Phase 4: Polish + Ship (2 weeks)**
- Memory palace builder
- Speech-to-text verification
- Export (cue sheets, PDFs)
- Deploy to Zo service

### 2.9 Open Questions

1. **Web Speech API accuracy for archaic language?** Masonic ritual uses 18th-century diction. May need Whisper for STT.
2. **FSRS tuning for passage-level items?** The algorithm was designed for atomic facts. Passage-level intervals may need custom parameters.
3. **Collaboration model?** If lodges/theatres adopt this, do they want shared passage libraries? Per-user progress tracking?
4. **Music licensing?** For song mode, backing tracks need to be either user-provided or generated (MIDI/synthesized).

---

## Sources

[^1]: Paivio, A. (1971). *Imagery and Verbal Processes*. Holt, Rinehart & Winston.
[^2]: Moll, B. & Sykes, E. (2023). "Optimized virtual reality-based Method of Loci memorization techniques." *Virtual Reality*, 27(2), 941-966. https://pmc.ncbi.nlm.nih.gov/articles/PMC9540171
[^3]: BBC Future (2020). "The surprising power of reading aloud." https://www.bbc.com/future/article/20200917-the-surprising-power-of-reading-aloud
[^4]: Wallace, W. T. (1994). "Memory for music: Effect of melody on recall of text." *Journal of Experimental Psychology: Learning, Memory, and Cognition*, 20(6), 1471-1485.
[^5]: University of Toulouse research on embodied learning for vocabulary acquisition.
[^6]: The Mindful Actor Workshops (2024). "The Actor's Memorization Toolbox: 12 Techniques." https://www.mindfulactorworkshops.com/blog/2024/1/24/the-actors-memorization-toolbox-12-techniques-to-turn-lines-into-second-nature
[^7]: Main, P. (2024). "8 Effective Memorization Techniques." Structural Learning. https://www.structural-learning.com/post/8-effective-memorization-techniques
[^8]: Alonso, I. et al. (2016). "Neural correlates of binding lyrics and melodies for the encoding of new songs." *NeuroImage*, 127. https://www.sciencedirect.com/science/article/abs/pii/S1053811915011313
[^9]: Woźniak, P. (1987). SM-2 Algorithm. https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge
[^10]: Expertium's Blog. "FSRS Benchmark." https://expertium.github.io/Benchmark.html
[^11]: SuperMemo. "Twenty Rules of Formulating Knowledge." https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge
