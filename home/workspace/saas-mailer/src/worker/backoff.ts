export function retryDelayMs(attempt: number, baseMs = 30_000, maxMs = 3_600_000): number {
  return Math.min(maxMs, baseMs * 2 ** Math.max(0, attempt - 1));
}

export function retryAt(attempt: number, now = new Date()): Date {
  return new Date(now.getTime() + retryDelayMs(attempt));
}
