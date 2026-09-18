---
name: agent-builder
description: Design and implement AI agents from a concrete use case through prompt, model, tools, memory, orchestration, interface, and evaluation decisions. Use when building a new agent or materially redesigning an existing one.
metadata:
  author: jaknyfe.zo.computer
---

# Agent Builder

## Usage

Use this skill before implementing a new agent or making a material redesign. Complete the eight stages in order, mark unnecessary stages as intentionally unused, and produce the required compact specification before implementation.

Build the smallest agent that can reliably complete the stated job. Treat the eight stages below as a design checklist, not a reason to add components the use case does not need.

## 1. Define purpose and scope

Write a one-sentence job statement. Identify the user, trigger, inputs, outputs, success criteria, constraints, and explicit out-of-scope behavior. Define what the agent may decide, what requires human approval, and what counts as completion.

## 2. Design the system prompt

Specify the agent's goal, role/persona, operating instructions, guardrails, tool-use rules, error behavior, and completion contract. Keep durable policy in the prompt; keep task data in runtime context. State assumptions clearly and require the agent to surface uncertainty when it affects the result.

## 3. Choose the LLM

Select the least expensive model that meets the quality and latency target. Compare reasoning quality, tool calling, context window, structured output, temperature/top-p controls, privacy or deployment location, and cost. Record why the selected model fits the workload and define a fallback only when it improves availability without changing safety or correctness requirements.

## 4. Design tools and integrations

Start with local functions or files. Add APIs, app integrations, MCP servers, agent-as-a-tool calls, or custom functions only when they remove a real limitation. For each tool define purpose, input schema, output shape, permissions, side effects, timeout, retry behavior, and failure message. Separate read-only tools from mutating tools and require approval at the boundary for consequential external actions.

## 5. Choose memory

Use episodic conversation history for the current task, working memory for temporary state, vector retrieval for semantic knowledge, SQL or structured storage for exact records, and file storage for durable artifacts. Define what is saved, retention, ownership, retrieval conditions, correction behavior, and how stale or conflicting memory is handled. Do not store secrets or sensitive data unless the design explicitly requires it and provides appropriate protection.

## 6. Add orchestration only as needed

Use a direct loop for simple tasks. Add routes or workflows for distinct paths, triggers for recurring or event-driven work, parameters for configurable behavior, queues for long-running or bursty work, and multiple agents only when roles genuinely need separation. Define state transitions, handoffs, retries, timeouts, idempotency, error handling, and the stop condition. Do not create a multi-agent system without a clear coordinator and measurable benefit.

## 7. Select the interface

Choose the smallest interface that matches the users and workflow: chat, web app, API endpoint, Slack or Discord bot, CLI, or another channel. Specify authentication, authorization, input validation, streaming or progress behavior, error presentation, accessibility, and the path from user request to visible completion. Verify the interface itself, not only the backend.

## 8. Test and evaluate

Create representative happy-path, edge-case, tool-failure, ambiguity, permission, and adversarial scenarios. Test unit behavior, tool contracts, latency, cost, output quality, safety boundaries, memory correctness, and recovery. Use a small golden set before broad testing. Define pass thresholds and an iteration loop: observe, diagnose, change one variable, rerun, and preserve the evidence.

## Required output

Before implementation, produce a compact agent specification containing:

- job, users, trigger, inputs, outputs, success criteria, and boundaries;
- system-prompt responsibilities and guardrails;
- model choice with quality, latency, context, privacy, and cost rationale;
- tool and integration table with permissions and failure behavior;
- memory policy and data stores;
- orchestration diagram or state flow when more than one step exists;
- interface contract;
- evaluation scenarios, metrics, thresholds, and definition of done.

Then implement the smallest viable slice, run the defined checks, and verify the user-facing result. If a stage is unnecessary, mark it intentionally unused with a reason instead of adding placeholder infrastructure.
