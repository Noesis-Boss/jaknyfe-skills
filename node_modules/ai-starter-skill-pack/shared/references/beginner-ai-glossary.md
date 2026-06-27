# Beginner AI Glossary

Plain-language definitions for this pack.

## LLM

A **large language model** is software trained to predict and generate language from patterns in large collections of data. It can write, summarize, classify, and reason imperfectly; it does not automatically know whether its answer is true.

## Model

The trained system that produces the output. Different models have different strengths, costs, limits, tools, and behavior.

## Chatbot

A conversational interface for interacting with a model. The chatbot may add memory, file handling, web access, safety rules, and other tools around the model.

## Agent

A model-based system that can pursue a goal through multiple steps, often by using tools, reading files, or changing a plan. “Agent” does not mean independent, trustworthy, or authorized; permissions and human checks still matter.

## Prompt

The instructions and context given to a model. A prompt may include a question, examples, documents, constraints, and a requested output format.

## Context window

The amount of information a model can consider in one interaction. A large context window is not perfect memory; important instructions can still be missed, and products may summarize or truncate content.

## Tool use

A model's ability to call an external function or service, such as web search, a calculator, a code runner, a calendar, or a database. A tool provides capability or data the model itself may not have.

## Retrieval

Finding relevant information from documents, databases, or search systems and supplying it to the model. Retrieval can improve grounding, but bad or incomplete sources still produce bad answers.

## Hallucination

A confident-looking output that is invented, unsupported, or wrong. Hallucinations can include fake citations, quotes, facts, calculations, or claims about tool access.

## Structured output

A response constrained to a predictable structure, often JSON that follows a schema. Native structured-output features are more reliable than merely asking for “valid JSON,” but the values still need checking.

## API

An **application programming interface** lets software send requests to another service in a defined format. An AI API is useful for building repeatable products or workflows, but it adds cost, security, error handling, and engineering work.

## Local model

A model that runs on a device or machine you control rather than only on a hosted service. Local models can support privacy, offline work, or customization, but they still require secure software, hardware, maintenance, and careful data handling.

## Workflow

A repeatable sequence that turns an input into a useful result. A workflow can include human steps, AI steps, checks, and approvals.

## Automation

A workflow in which some steps run automatically. Good automation has clear inputs, failure handling, logs, permissions, and a human stop or approval point when risk is meaningful.

## Embeddings

Numerical representations that place semantically related content near each other. They are often used for search, clustering, recommendations, and retrieval.

## Fine-tuning

Additional training that changes a model's behavior using curated examples. It is not the first fix for most beginner problems; clearer instructions, examples, retrieval, or a better workflow are often simpler.

## One useful distinction

- A **prompt** asks for one interaction.
- A **workflow** connects repeatable steps.
- An **agent** may choose and execute steps.
- An **automation** runs steps with less manual effort.

Start with the smallest level that solves the real problem.
