# Chapter 13 research: compound knowledge — your substrate as an asset

## Peer-Reviewed studies

### 1. knowledge compounding under the agentic ROI framework
**Citation:** Wei et al., "Knowledge Compounding: An Empirical Economic Analysis of Self-Evolving Knowledge Wikis under the Agentic ROI Framework," arXiv:2604.11243, 2025. https://doi.org/10.48550/arxiv.2604.11243

**Summary:** This paper formally reclassifies a subset of LLM-generated tokens from consumables to capital goods, shifting the analytic frame from per-query marginal cost to dynamic capital accumulation. Using "Qing Claw," a minimal 200-line reference implementation of the LLM Wiki paradigm, the authors compare compounding, chunk-RAG, and long-context baselines across four queries. Although the compounding method used ~47K tokens per query (vs. 3.4K for chunk-RAG and 305K for long-context), it produced four answers, one synthesis page, and five new persistent entity facts written into a queryable knowledge base. The findings demonstrate that despite higher immediate token cost, knowledge compounding yields durable, reusable outputs that strictly stateless methods cannot produce—a structural advantage that widens with each query.

### 2. governing AI agents as organizational portfolios
**Citation:** Tanaka et al., "Governing Agentic AI as Organizational Portfolios for Sustained Value: Evidence from a Japanese Industrial Conglomerate," *AI & Society*, 2026. https://doi.org/10.1177/23949643261450309

**Summary:** A comparative analysis of five AI agent deployments within a Japanese industrial conglomerate demonstrates that value from agentic AI scales only when governance shifts from building isolated tools to assetizing and coordinating agents as a portfolio ("System of Agents"). Centralized adoption alone was insufficient; sustained value required standardized logging, reusable artefacts, cross-project learning routines, and portfolio-level decision rights. Firms that govern their agents as reusable assets realized compounding productivity gains that outpaced isolated-agent deployments, while those that treated each agent as a one-off project saw diminishing returns and knowledge attrition.

### 3. cross-Domain agent knowledge bases for reuse
**Citation:** "Agent KB: Leveraging Cross-Domain Experience for Agentic Problem Solving," arXiv:2507.06229, 2025. https://doi.org/10.48550/arxiv.2507.06229

**Summary:** AGENT KB is a framework-agnostic knowledge base that captures and reuses execution experiences across heterogeneous agent systems via a Reason-Retrieve-Refine cycle. Experiences are standardized into a lightweight REST-addressable schema, enabling diverse agents to contribute to and draw from a shared memory without architectural changes. The knowledge base is self-evolving—growing via addition, deduplication, and eviction—to accumulate reusable trajectories. Empirical evaluations across GAIA, Humanity's Last Exam, GPQA, and SWE-bench showed notable performance gains across multiple frameworks and model families, providing direct evidence that cross-domain reuse of captured agent experience compounds into measurable capability improvements.

### 4. skill libraries as non-Parametric agent memory
**Citation:** "Memento-Skills: Let Agents Design Agents," arXiv:2603.18743, 2026. https://doi.org/10.48550/arxiv.2603.18743

**Summary:** Memento-Skills treats executable skills as external memory units that evolve into a growing, persistent skill library. Through a Read–Write Reflective Learning loop, agents autonomously acquire, refine, and reuse skills from deployment experience without updating underlying LLM parameters. A behavior-aligned, offline-RL router selects the most effective skills per task. The framework demonstrates continual improvement on GAIA and HLE benchmarks, showing that a frozen LLM, when paired with an expanding portfolio of versioned capabilities, outperforms agents without accumulated skills. The contribution reframes skills as non-parametric knowledge assets—the primary vehicle for cumulative learning rather than model weight updates.

### 5. meta-Analysis learning loops for self-Improving agent systems
**Citation:** "Meta-Analysis Learning Loop: Experimental Validation of Self-Improving Agent Orchestration Systems," OSF, 2026. https://doi.org/10.17605/osf.io/vgyec

**Summary:** This study experimentally validates that structured post-session meta-analysis of agent development sessions creates a cumulative knowledge base yielding compounding efficiency gains. Within a single six-task project, the system achieved ~49% fewer execution turns and up to 73% time savings. Cross-project transfer across three independent projects (CLI parser, file utilities, string utilities) produced ~42% efficiency gains with a 63.2% pattern reuse rate via reference-based transfer. All 1,838 tests passed (100% quality retention). Infrastructure-oriented patterns (documentation, testing, error handling) showed 60–67% reuse portability, while domain-specific logic remained project-bound—quantifying precisely which knowledge compounds across an agent ecosystem and which does not.

## Compelling statistics

1. **Enterprise agentic AI delivers 300–400% ROI over 1–3 years.** A multi-firm case study analysis across logistics, finance, HR, and customer-service deployments found that agentic architectures produce compounding ROI well in excess of the initial year's gains, as agents optimize and reuse learned behaviors across processes. Source: *International Journal of Enterprise Research and Engineering Technology*, "From Intelligent Automation to Agentic AI," 2026. https://doi.org/10.63282/3050-922x.ijeret-v5i4p114

2. **Generalist enterprise agents cut development costs 50% and development time 90%.** IBM's CUGA generalist agent, evaluated against task-specific baselines on a 26-task enterprise benchmark, approached hand-crafted agent accuracy while reducing development cost by up to 50% and development time by up to 90%. Source: AAAI, "From Benchmarks to Business Impact: Deploying IBM Generalist Agent in Enterprise Production," 2026. https://doi.org/10.1609/aaai.v40i47.41485

3. **AI agent autonomy cuts task time 87% and cost 94% across 18 domains.** A cross-domain study comparing autonomous AI agents to Search + Human baselines showed total task time dropping from 269 minutes to 36 minutes (87% reduction) and cost from labor-dominated to AI-dominated, yielding a 94% cost reduction. AI-assisted workflows cut dissatisfaction by 55% versus search. Source: arXiv, "How AI Agents Reshape Knowledge Work," 2026. https://doi.org/10.48550/arxiv.2606.07489

## Expert quotations

**On the substrate as the hard part:**

> "Fun demos show what an agent can do, but only architecture shows how it stays reliable. The real leap won't come from letting an LLM run loose, but from giving it a stable memory substrate, sustained context, and a cognitive loop it can rely on. Autonomy is easy. Continuity is the hard part."
> — **Andrew Ng**, Founder of DeepLearning.AI and AI Fund, on building production agents (LinkedIn, 2025) https://www.linkedin.com/posts/andrewyng_sharing-a-fun-recipe-for-building-a-highly-activity-7404934836232052736

**On intelligence as a compounding asset:**

> "The larger insight is that intelligence compounds. Surround a group with more intelligence—be it in the form of talented colleagues or AI copilots—and their collective imagination broadens… If the global economy is 55%–65% driven by human intelligence, then multiplying the productivity of that intelligence via AI doesn't shrink opportunity; it unlocks trillions."
> — **Jensen Huang**, CEO of NVIDIA, BG2 Podcast with Brad Gerstner and Bill Gurley, 2025 https://www.wisdomtree.com/us/insights/blog/jensen-huang-and-the-billion-fold-future-of-intelligence

## Real-World case study: the japanese industrial conglomerate's "System of agents"

A peer-reviewed study of a large Japanese industrial conglomerate analyzed five AI agent deployments ranging from isolated model-focused tools to a portfolio-governed "System of Agents" (SoA). The findings are the clearest enterprise demonstration of the substrate-as-asset thesis in the current literature.

The early deployments treated each agent as a bespoke tool—one per problem domain. Each delivered isolated returns, but exhibited the classic pathologies of an unreused asset portfolio: no knowledge transfer across deployments, governance reinvented each time, and capability that did not compound. The breakthrough came when governance shifted to the portfolio level—standardized logging, reusable artefacts, consolidated decision rights under a portfolio authority empowered to force cross-project reuse. Agents were "assetized"—packaged with documentation, traceable behaviour, and retrieval interfaces so any new project could draw on accumulated capabilities.

The result: sustained, compounding value the isolated-agent approach had structurally failed to produce. Critically, centralized adoption of the SoA model was insufficient by itself—the durable returns emerged only from assetization, standardized traceability, and enforced reuse governance. Firms that merely adopted agents without instituting the portfolio disciplines saw no compounding; firms that governed their agents as reusable assets saw returns that scaled across growing agent fleets (Tanaka et al., *AI & Society*, 2026).

This case is the empirical anchor for the chapter's claim: the substrate—not the individual agent—is the asset. Value persists and compounds only to the extent that agents leave behind queryable, reusable, versioned residue.

## Synthesis

The case for substrate compounding rests on a convergence of formal models, empirical agent research, and enterprise evidence. The Agentic ROI framework (Wei et al., 2025) provides the formal grounding: when tokens are reclassified from consumables to capital goods, the long-horizon economics flip—interactions yield durable, queryable residue whose value does not decay with reuse. The cross-domain knowledge-base (Agent KB, 2025) and skill-library (Memento-Skills, 2026) studies prove this mechanism operationally; the meta-analysis loop study quantifies it with rare precision—reuse rates above 60% for infrastructure patterns with 100% quality retention. The throughline from first study to last: the substrate—not the model, not the agent, not the prompt—is the asset whose value compounds with each use.

Expert judgment reinforces the experiments. Andrew Ng defines the architectural bottleneck: continuity—the stable memory substrate, sustained context, and reliable cognitive loop—is the harder problem than autonomy, the one that creates durable agent value. Jensen Huang articulates the macro corollary: intelligence compounds at the system level. Neither claim is speculative—both are consistent with enterprise evidence showing 300–400% ROI over multi-year horizons when governance enforces assetization and reuse (Tanaka et al., 2026).

The 1000-day view follows naturally. The first 100 days build a single working agent and a thin substrate. Days 100–500 begin paying back—the agent's residue accelerates the next agent. Days 500–1000 show compounding—the portfolio of versioned assets makes the marginal agent cheaper, faster, more reliable. By Day 1000, the substrate is the defensible position: hard to build, hard to copy, impossible to acquire without traversing the same experiential arc. Exit-value thinking translates this into a single proposition—an asset that compounds costs less per unit of output the longer you hold it, and is valued on the cash flows it generates across its full portfolio of versions, not the cost of any single deployment. The portfolio of versioned agents is the substrate made legible: the asset class that captures the compounding for whoever owns the substrate.
