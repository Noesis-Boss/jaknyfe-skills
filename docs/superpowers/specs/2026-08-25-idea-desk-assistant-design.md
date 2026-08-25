# Idea Desk Assistant Design

## Objective

Make **Ask assistant about this idea** return a real AI analysis for the selected Idea Desk item and support contextual follow-up questions in a modal.

## Existing behavior to preserve

- Live and demo idea loading through `/api/idea-desk`.
- Feed scanning, source filters, minimum-score filtering, sorting, selection, and current styling.
- Private visibility of `/idea-desk`.

## Architecture

Create a dedicated public-network API route at `/api/idea-desk/ask`. The page sends only the selected idea fields and the current follow-up message. The server builds the trusted analysis prompt, calls the Zo Ask API using `ZO_API_KEY`, and returns JSON. No secret or system prompt reaches the browser.

The first request asks for a concise structured assessment covering viability, target audience, best content format, differentiation, risks, and one concrete next action. Follow-up requests include the selected idea and the prior assistant answer so the conversation remains scoped without adding persistent storage.

## Interface

Clicking the existing button opens a modal and immediately starts analysis. The modal contains the selected idea title, a loading state, the assistant response, an error-and-retry state, a follow-up input, and a send button. It closes through its close button, backdrop click, or Escape. Focus remains usable by keyboard and the background is visually de-emphasized.

## Data flow

1. The page opens the modal and POSTs `{ idea, question, priorAnswer }` to `/api/idea-desk/ask`.
2. The API validates required idea fields and caps user-controlled text lengths.
3. The API calls `https://api.zo.computer/zo/ask` with the server-side token and an Idea Desk-specific prompt.
4. The API returns `{ answer }`; upstream or configuration failures return a safe JSON error with an appropriate status.
5. A follow-up repeats the request with the same idea context and prior answer.

## Error handling

- Missing `ZO_API_KEY`: return a configuration error without exposing secrets.
- Invalid input: return HTTP 400.
- Zo timeout or non-JSON response: return HTTP 502 with retryable UI copy.
- Disable duplicate sends while a request is active.
- Clear modal conversation when a different idea is opened.

## Verification

- Confirm the initial button opens the modal and produces a non-placeholder AI response tied to the selected idea.
- Ask one follow-up and confirm the answer retains the idea context.
- Confirm loading, retry, close button, backdrop close, and Escape behavior.
- Confirm scans, filters, sorting, and idea selection still work.
- Check Space runtime errors and capture a screenshot showing the rendered assistant response before declaring completion.

## Definition of done

The private Idea Desk page visibly returns a real, idea-specific AI analysis in a modal, accepts a contextual follow-up, handles errors without breaking the dashboard, and passes screenshot-based verification.
