export type ParsedContact = {
  email: string;
  first_name?: string;
  last_name?: string;
  custom_fields: Record<string, string>;
};

export class InvalidContactsCsvError extends Error {}

function normalizeHeader(value: string): string {
  return value.trim().toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "");
}

const headerAliases = {
  email: ["email", "email_address", "e_mail", "mail", "work_email", "primary_email", "email_1_value", "email_2_value", "email_3_value", "email_4_value", "email_5_value", "email_value", "e_mail_1_value", "e_mail_2_value", "e_mail_3_value", "e_mail_4_value", "e_mail_5_value", "e_mail_value"],
  first_name: ["first_name", "firstname", "first", "given_name", "givenname", "fname"],
  last_name: ["last_name", "lastname", "last", "surname", "family_name", "familyname", "lname"],
  full_name: ["full_name", "fullname", "name", "contact_name", "display_name"],
} as const;

function findHeader(headers: string[], field: keyof typeof headerAliases): number {
  return headers.findIndex((header) => (headerAliases[field] as readonly string[]).includes(header));
}

function parseRows(text: string): string[][] {
  const delimiter = detectDelimiter(text);
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    if (quoted) {
      if (char === '"' && text[i + 1] === '"') { field += '"'; i += 1; }
      else if (char === '"') quoted = false;
      else field += char;
    } else if (char === '"' && field.length === 0) quoted = true;
    else if (char === '"') throw new InvalidContactsCsvError("Malformed CSV: stray quote");
    else if (char === delimiter) { row.push(field); field = ""; }
    else if (char === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
    else if (char !== "\r") field += char;
  }
  if (quoted) throw new InvalidContactsCsvError("Malformed CSV: unterminated quote");
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows.filter((candidate) => candidate.some((value) => value.trim() !== ""));
}

function detectDelimiter(text: string): string {
  const firstLine = text.split(/\r?\n/).find((line) => line.trim() !== "") || "";
  const candidates = [",", ";", "\t", "|"];
  return candidates.reduce((best, candidate) => {
    let count = 0;
    let quoted = false;
    for (const char of firstLine) {
      if (char === '"') quoted = !quoted;
      else if (!quoted && char === candidate) count += 1;
    }
    return count > best.count ? { candidate, count } : best;
  }, { candidate: ",", count: 0 }).candidate;
}

function validEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function parseContactsCsv(csvText: string): ParsedContact[] {
  const rows = parseRows(csvText);
  if (!rows.length) return [];
  const headers = rows[0].map((header, index) => normalizeHeader(index === 0 ? header.replace(/^\uFEFF/, "") : header));
  const emailIndex = findHeader(headers, "email");
  if (emailIndex < 0) throw new InvalidContactsCsvError("Invalid CSV: missing required email header");
  const firstNameIndex = findHeader(headers, "first_name");
  const lastNameIndex = findHeader(headers, "last_name");
  const fullNameIndex = findHeader(headers, "full_name");
  return rows.slice(1).flatMap((values) => {
    const email = (values[emailIndex] || "").trim().toLowerCase();
    if (!validEmail(email)) return [];
    const fullName = fullNameIndex >= 0 ? (values[fullNameIndex] || "").trim() : "";
    const nameParts = fullName.split(/\s+/).filter(Boolean);
    const first_name = (firstNameIndex >= 0 ? values[firstNameIndex] : nameParts[0])?.trim() || undefined;
    const last_name = (lastNameIndex >= 0 ? values[lastNameIndex] : nameParts.slice(1).join(" "))?.trim() || undefined;
    const custom_fields: Record<string, string> = {};
    headers.forEach((header, index) => {
      if (header && ![emailIndex, firstNameIndex, lastNameIndex, fullNameIndex].includes(index)) custom_fields[header] = (values[index] || "").trim();
    });
    return [{ email, first_name, last_name, custom_fields }];
  });
}

export function countInvalidContacts(csvText: string): number {
  const rows = parseRows(csvText);
  if (!rows.length) return 0;
  const headers = rows[0].map((header, index) => normalizeHeader(index === 0 ? header.replace(/^\uFEFF/, "") : header));
  const emailIndex = findHeader(headers, "email");
  if (emailIndex < 0) throw new InvalidContactsCsvError("Invalid CSV: missing required email header");
  return rows.slice(1).filter((row) => !validEmail((row[emailIndex] || "").trim())).length;
}
