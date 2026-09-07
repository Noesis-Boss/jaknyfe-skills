# LLC Builder Design

## Scope

Create a reusable Zo skill that turns a business profile into a state-aware LLC formation and funding-readiness package. It supports all U.S. states plus generic federal guidance and produces Markdown plus a downloadable document packet.

## Behavior

The skill collects entity, ownership, industry, operating-state, banking, credit, revenue, and funding information; researches current authoritative sources; separates facts from assumptions; and produces formation, compliance, funding-readiness, credit-building, operating-agreement, banking, and source documents.

## Web output

Each run creates a unique public Space page under `/llc-builder/<normalized-business-slug>`. The page displays the generated sections and links to each file and the complete package. The homepage remains unchanged.

## Guardrails

The output is educational and includes attorney/CPA review warnings. It must not recommend misrepresentation or promise funding, tax, legal, or credit outcomes.
