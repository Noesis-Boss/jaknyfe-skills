export type TenantRateLimiter = { tryAcquire: (organizationId: string, now?: number) => boolean; visible: (organizationId: string, now?: number) => number };

export function createTenantRateLimiter(limitPerMinute: number): TenantRateLimiter {
  const windows = new Map<string, number[]>();
  return {
    tryAcquire(organizationId, now = Date.now()) {
      const windowStart = now - 60_000;
      const hits = (windows.get(organizationId) || []).filter(time => time > windowStart);
      if (hits.length >= limitPerMinute) {
        windows.set(organizationId, hits);
        return false;
      }
      hits.push(now);
      windows.set(organizationId, hits);
      return true;
    },
    visible(organizationId, now = Date.now()) {
      return (windows.get(organizationId) || []).filter(time => time > now - 60_000).length;
    },
  };
}
