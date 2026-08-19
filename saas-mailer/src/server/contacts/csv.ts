export type ParsedContact = {
  email: string;
  first_name?: string;
  last_name?: string;
  custom_fields: Record<string, string>;
};

export class InvalidContactsCsvError extends Error {}

function normalizeHeader(value: string): string {
  return value.trim().toLowerCase().replace(/[ -]+/g, "_");
}

function parseRows(text: string): string[][] {
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
    else if (char === ",") { row.push(field); field = ""; }
    else if (char === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
    else if (char !== "\r") field += char;
  }
  if (quoted) throw new InvalidContactsCsvError("Malformed CSV: unterminated quote");
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows.filter((candidate) => candidate.some((value) => value.trim() !== ""));
}

function validEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function parseContactsCsv(csvText: string): ParsedContact[] {
  const rows = parseRows(csvText);
  if (!rows.length) return [];
  const headers = rows[0].map((header, index) => normalizeHeader(index === 0 ? header.replace(/^\uFEFF/, "") : header));
  const emailIndex = headers.indexOf("email");
  if (emailIndex < 0) throw new InvalidContactsCsvError("Invalid CSV: missing required email header");
  return rows.slice(1).flatMap((values) => {
    const email = (values[emailIndex] || "").trim().toLowerCase();
    if (!validEmail(email)) return [];
    const custom_fields: Record<string, string> = {};
    headers.forEach((header, index) => {
      if (header && !["email", "first_name", "last_name"].includes(header)) custom_fields[header] = (values[index] || "").trim();
    });
    return [{ email, first_name: values[headers.indexOf("first_name")]?.trim() || undefined, last_name: values[headers.indexOf("last_name")]?.trim() || undefined, custom_fields }];
  });
}

export function countInvalidContacts(csvText: string): number {
  const rows = parseRows(csvText);
  if (!rows.length) return 0;
  const headers = rows[0].map((header, index) => normalizeHeader(index === 0 ? header.replace(/^\uFEFF/, "") : header));
  const emailIndex = headers.indexOf("email");
  if (emailIndex < 0) throw new InvalidContactsCsvError("Invalid CSV: missing required email header");
  return rows.slice(1).filter((row) => !validEmail((row[emailIndex] || "").trim())).length;
}
