## Peer-Reviewed studies (5)
1. **Sparrow, Liu & Wegner (2011), *Science* 333: 776–778** — Internet becomes a transactive memory store; participants recall *location* better than *content* when they trust external storage. Foundational empirical case for offloading.
2. **Risko & Gilbert (2016), *Trends in Cognitive Sciences* 20(9): 676–688** — Cognitive offloading is task-dependent; the real benefit is *released working-memory capacity for other tasks*, not preservation of the saved item.
3. **Storm & Stone (2015), *Psychological Science* 26(2): 182–188** — Saving info to a computer before studying new material improves recall of the *new* material; offloading reduces proactive interference.
4. **Lewis et al. (2020), *NeurIPS* 33: 9459–9474** — RAG (parametric + non-parametric retrieval) produces more factual, specific, diverse outputs than parametric-only models. The technical analog of the chapter's argument.
5. **TREC benchmarks (NIST), summarized in embeddingstack.com** — Dense embedding retrieval beats BM25 keyword baselines by 30–50%. Embeddings encode meaning, not tokens — the retrieval-cost flipper.

## Statistics (2)
- **1.8 hrs/day (9.3 hrs/week)** searching for info — McKinsey Global Institute, *The Social Economy* (2012). One in five salaried hours lost.
- **2.5 hrs/day (~30%)** searching — IDC white paper. Corroborated independently by Gartner 2023: 47% of digital workers struggle to find info; average document location takes 18 min.

## Expert quotations (2)
- *David Allen*: "Your mind is for having ideas, not holding them." (*Getting Things Done*, 2001, p. 277 — registered trademark of David Allen Company.)
- *Lewis et al.* (2020, NeurIPS, p. 9474): "RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline."

## Real-World case study
**NASA Lessons Learned Information System → knowledge graph.** David Meza's team converted LLIS from keyword search (endless ranked links across 20M documents, <1% being lessons) into a semantic knowledge graph. Single natural-language query replaced one-by-one document inspection; consultation rates rose after a decade of disuse. NASA didn't lack the knowledge — it lacked a substrate cheap enough to query. Full OIG citation: IG-12-012 (2012).

## Synthesis
The arc: offloading frees capacity (Sparrow, Risko & Gilbert, Storm & Stone) → embeddings drop query cost 30–50% over keyword baselines (TREC) → RAG beats recall-only on factual grounding (Lewis). The inflection point is embeddings. Below the cost threshold, external memory stays a *second inbox* (a pile you owe attention to); above it, query cost drops below recall cost and the substrate becomes invisible. You stop remembering *where* you wrote the thing and start *thinking with* it.

[^1]: Sparrow, B., Liu, J. & Wegner, D. M. (2011). Google Effects on Memory: Cognitive Consequences of Having Information at Our Fingertips. *Science*, 333(6040), 776–778.
[^2]: Risko, E. F. & Gilbert, S. J. (2016). Cognitive Offloading. *Trends in Cognitive Sciences*, 20(9), 676–688.
[^3]: Storm, B. C. & Stone, S. M. (2015). Saving-Enhanced Memory: The Benefits of Saving on the Learning and Remembering of New Information. *Psychological Science*, 26(2), 182–188.
[^4]: Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS* 33: 9459–9474.
[^5]: embeddingstack.com service-selection survey, citing NIST Text REtrieval Conference (TREC) tracks. https://embeddingstack.com/semantic-search-technology-services
[^6]: McKinsey Global Institute (2012). *The Social Economy: Unlocking value and productivity through social technologies*.
[^7]: IDC white paper, *Information: The Lifeblood of the Enterprise*.
[^8]: Allen, D. (2001). *Getting Things Done: The Art of Stress-Free Productivity*. Penguin, p. 277.
[^9]: NASA Office of Inspector General (2012). *Review of NASA's Lessons Learned Information System*, IG-12-012. https://oig.nasa.gov/docs/IG-12-012.pdf
[^10]: Nuclino (2023). *Why NASA converted its lessons learned database into a knowledge graph*. https://blog.nuclino.com/why-nasa-converted-its-lessons-learned-database-into-a-knowledge-graph
