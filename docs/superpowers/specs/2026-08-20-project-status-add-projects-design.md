# Add Projects from Project Status

## Goal
Allow the private `/project-status` page to accept a natural-language prompt that proposes updates to an existing project or creates a new project.

## Behavior
- An “Add project” button opens a modal with a multiline prompt input.
- “Evaluate prompt” parses explicit fields using simple local heuristics.
- Existing project names are matched case-insensitively.
- New projects receive safe defaults for omitted fields.
- The modal shows a preview before applying changes.
- Apply updates the in-memory registry for the current browser session.
- Cancel, Escape, and backdrop click close the modal.
- No API, external model, dependency, or persistence is added.

## Safety
- No changes apply until the user clicks Apply changes.
- Unspecified existing fields remain unchanged.
- New records require a project name and use visible defaults.
- Parsing failures show a clear error and preserve the modal input.

## Verification
- Screenshot confirms button, modal, prompt, and preview.
- Browser interaction confirms an existing-project update and a new-project add.
- Existing filters and reset behavior continue to work.
