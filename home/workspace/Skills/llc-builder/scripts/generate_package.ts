#!/usr/bin/env bun

type Profile = {
  businessName: string;
  formationState?: string;
  operatingStates?: string[];
  industry?: string;
  website?: string;
  owners?: string;
  fundingGoal?: string;
  facts?: string[];
};

const input = Bun.argv[2];
if (!input) {
  console.error("Usage: bun generate_package.ts profile.json");
  process.exit(1);
}

const profile = JSON.parse(await Bun.file(input).text()) as Profile;
const slug = profile.businessName.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const out = `${slug}-llc-builder-package`;
await Bun.write(`${out}/01-executive-summary.md`, `# ${profile.businessName}\n\n## Executive summary\n\nThis package is a planning draft for ${profile.businessName}. Verify all legal, tax, licensing, and lending requirements with qualified professionals.\n\n- Formation state: ${profile.formationState || "Not provided"}\n- Operating states: ${(profile.operatingStates || []).join(", ") || "Not provided"}\n- Industry: ${profile.industry || "Not provided"}\n- Funding goal: ${profile.fundingGoal || "Not provided"}\n\n## Facts to verify\n\n${(profile.facts || ["No verified facts supplied."]).map((fact) => `- ${fact}`).join("\n")}\n`);
await Bun.write(`${out}/02-formation-and-compliance-plan.md`, `# Formation and compliance plan\n\n## Required research\n\n- Confirm formation-state filing requirements and fees.\n- Confirm registered-agent and annual-report requirements.\n- Confirm foreign qualification in each operating state.\n- Confirm federal, state, county, and city licenses.\n- Confirm EIN and tax registrations.\n\n## Open items\n\n- Ownership and management structure\n- Operating agreement terms\n- Business banking setup\n- Insurance coverage\n`);
await Bun.write(`${out}/03-funding-readiness-analysis.md`, `# Funding-readiness analysis\n\n## Product fit\n\nEvaluate revenue-based financing, business lines of credit, and 0% business credit cards only against verified revenue, time in business, cash flow, personal credit, and repayment capacity.\n\n## Underwriting risks\n\n- Missing or inconsistent business identity data\n- Insufficient documented revenue or banking history\n- Weak business-credit reporting history\n- Industry, licensing, or entity-purpose mismatch\n\nNo funding outcome is guaranteed.\n`);
await Bun.write(`${out}/04-business-credit-building-plan.md`, `# Business-credit building plan\n\n1. Establish consistent legal identity across state, IRS, banking, and directories.\n2. Open and use a dedicated business bank account.\n3. Obtain appropriate vendor or secured trade lines.\n4. Confirm reporting to commercial bureaus before relying on an account.\n5. Pay on time and reconcile monthly.\n`);
await Bun.write(`${out}/05-operating-agreement-draft.md`, `# Operating agreement draft\n\nThis is a non-final template. Have an attorney adapt it to the formation state, ownership, tax election, management structure, contributions, distributions, transfers, and dissolution terms.\n\n## Company\n\n- Name: ${profile.businessName}\n- Formation state: ${profile.formationState || "[INSERT]"}\n- Owners: ${profile.owners || "[INSERT]"}\n\n## Required attorney decisions\n\n- Member-managed or manager-managed\n- Voting thresholds\n- Capital contributions\n- Distributions and tax allocations\n- Transfer, buyout, dispute, and dissolution provisions\n`);
await Bun.write(`${out}/06-initial-resolutions-and-banking-checklist.md`, `# Initial resolutions and banking checklist\n\n- Approve formation documents.\n- Adopt the operating agreement.\n- Authorize EIN and tax registrations.\n- Authorize business bank account and signers.\n- Approve accounting method and records policy.\n- Obtain required licenses and insurance.\n- Keep formation, banking, tax, and ownership records together.\n`);
await Bun.write(`${out}/07-state-and-federal-sources.md`, `# State and federal sources\n\nAdd current official Secretary of State, state tax, licensing, IRS, FinCEN, SBA, and lender sources here. Record the page title, URL, access date, and requirement supported.\n`);
console.log(`${process.cwd()}/${out}`);
