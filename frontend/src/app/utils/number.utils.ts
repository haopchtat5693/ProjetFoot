export function toNumberOrNull(value: number | string | null): number | null {
  if (value === null || value === '') return null;

  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}
