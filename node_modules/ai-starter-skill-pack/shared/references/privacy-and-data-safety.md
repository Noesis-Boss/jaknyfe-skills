# Privacy and Data Safety

**Last reviewed:** 2026-06-23

This is a practical baseline, not legal, medical, security, compliance, or benefits advice. Product settings and organizational rules change.

## Do not paste these into an AI tool

Unless a specifically approved system, policy, and task require it, do not paste:

- passwords, recovery codes, API keys, access tokens, private keys, or session cookies;
- Social Security or national ID numbers;
- full birth dates paired with identity details;
- bank, card, tax, payroll, or credit-account records;
- unredacted medical, therapy, disability, legal, immigration, or benefits records;
- private client, patient, student, employee, or customer information;
- confidential employer documents, source code, trade secrets, or incident data;
- children's personal information;
- intimate images or private communications;
- someone else's personal data without authority to use it.

Never put a secret into a prompt merely to “see whether it works.” Treat exposed credentials as compromised and rotate them through the proper system.

## Use minimum necessary context

Before sharing content:

1. State the task without the sensitive material.
2. Ask whether a synthetic example is enough.
3. Extract only the paragraph or fields needed.
4. Replace identifiers with consistent placeholders.
5. Remove hidden metadata and comments where practical.
6. Check employer, school, client, platform, and legal rules.
7. Review the final prompt one more time before submitting.

Example:

```text
Bad:
Jane Doe, SSN 123-45-6789, has a balance of $8,442 at Example Bank...

Safer:
[CLIENT_A] has an unsecured balance of [AMOUNT] at [LENDER_A]...
```

For numerical analysis, preserve relationships while changing identifying values when exact figures are not required.

## Redaction checklist

Replace or remove:

- names and usernames;
- addresses and exact locations;
- account, case, ticket, student, employee, or patient numbers;
- phone numbers and email addresses;
- dates that identify a person;
- company or client names under confidentiality;
- document properties, tracked changes, comments, and image metadata;
- unique combinations that can re-identify someone.

“Anonymous” is not the same as safe. A rare job title, town, diagnosis, and date can identify a person even without a name.

## Consumer, work, school, and API accounts differ

Do not assume that one vendor has one data policy.

Consumer chats, temporary/private modes, business plans, education plans, enterprise products, and APIs may differ in:

- whether content can be used for model improvement;
- retention periods;
- administrator access;
- human review;
- regional processing;
- available controls;
- contractual protections.

Check the current policy for the exact product and account type. Turning off training does not necessarily mean zero retention or zero authorized access.

## When local or offline tools may be appropriate

Consider a properly secured local or offline workflow when:

- policy requires data to stay on an approved device or network;
- the material is too sensitive for a hosted service;
- internet access is unavailable or inappropriate;
- the organization has approved a specific local model and configuration.

Local does not automatically mean private. Check:

- where the model came from;
- whether the app calls external services;
- logs and telemetry;
- plugins and extensions;
- disk encryption and user access;
- backups and sync folders;
- malware and supply-chain risk;
- whether the device itself is managed and approved.

## When to avoid AI

Avoid or pause AI use when:

- you do not have permission to use the data;
- a school, employer, client, or professional rule forbids it;
- the task requires a licensed professional's judgment;
- an unverified output could directly harm someone's health, rights, finances, employment, housing, or safety;
- the model would make a consequential final decision about a person;
- the action is irreversible and lacks human review;
- you cannot explain or check the result;
- the benefit is trivial compared with the privacy risk.

AI can help organize questions for a qualified professional. It should not impersonate one.

## Safe defaults for this pack

- Begin with public, synthetic, or redacted material.
- Ask for the least sensitive input that can solve the problem.
- Keep a human approval step before external actions.
- Label uncertain or generated content.
- Verify important claims with current primary sources.
- Do not upload files “just in case.”
- Do not retain sensitive examples in a learning log.

## Source links

Vendor controls should be rechecked at the time of use:

- OpenAI data controls: https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance
- Anthropic consumer model-improvement controls: https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings
- Anthropic commercial data policy: https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training
- Google Gemini Apps Privacy Hub: https://support.google.com/gemini/answer/13594961
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
