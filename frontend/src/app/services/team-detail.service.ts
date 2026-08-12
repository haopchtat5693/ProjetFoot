import { Injectable } from '@angular/core';

export interface StatBreakdown {
  label: string;
  home?: string;
  away?: string;
  total?: string;
}

@Injectable({ providedIn: 'root' })
export class TeamDetailService {
  extractTotal(value: unknown): string {
    if (value === null || value === undefined) return '—';
    if (typeof value === 'number') return String(value);
    if (typeof value !== 'object') return this.formatValue(value);

    const obj = value as Record<string, unknown>;
    if ('total' in obj) {
      const total = obj['total'];
      if (typeof total === 'number') return String(total);
      if (typeof total === 'object' && total !== null) return this.extractTotal(total);
    }

    for (const val of Object.values(obj)) {
      if (typeof val === 'object' && val !== null) {
        const nested = val as Record<string, unknown>;
        if ('total' in nested) {
          const total = nested['total'];
          if (typeof total === 'number') return String(total);
          if (typeof total === 'object' && total !== null) return this.extractTotal(total);
        }
      }
    }

    for (const val of Object.values(obj)) {
      if (typeof val === 'number') return String(val);
    }

    return this.formatValue(value);
  }

  formatValue(value: unknown): string {
    if (value === null || value === undefined || value === '') return '—';
    if (Array.isArray(value)) return value.length ? `${value.length}` : '—';
    if (typeof value === 'object') {
      return Object.entries(value as Record<string, unknown>)
        .map(([key, nestedValue]) => `${key}: ${this.formatValue(nestedValue)}`)
        .join(' · ');
    }
    return String(value);
  }

  createBreakdown(label: string, value: unknown): StatBreakdown {
    return { label, ...this.extractBreakdownValue(value) };
  }

  createCardBreakdown(label: string, cards: unknown, color: 'yellow' | 'red'): StatBreakdown {
    if (!cards || typeof cards !== 'object') return { label, total: '—' };

    const cardsObj = cards as Record<string, unknown>;
    if (!(color in cardsObj)) return { label, total: '—' };

    const colorObj = cardsObj[color] as Record<string, unknown>;
    let total = 0;

    for (const timePeriodObj of Object.values(colorObj)) {
      if (typeof timePeriodObj === 'object' && timePeriodObj !== null) {
        const timePeriod = timePeriodObj as Record<string, unknown>;
        if ('total' in timePeriod && typeof timePeriod['total'] === 'number') {
          total += timePeriod['total'];
        }
      }
    }

    return { label, total: total > 0 ? String(total) : '—' };
  }

  createSimplePenaltyBreakdown(label: string, penalty: unknown): StatBreakdown {
    if (!penalty || typeof penalty !== 'object') return { label, total: '—' };

    const penaltyObj = penalty as Record<string, unknown>;
    let scored = 0;
    let total = 0;

    if ('scored' in penaltyObj && typeof penaltyObj['scored'] === 'object' && penaltyObj['scored'] !== null) {
      const scoredObj = penaltyObj['scored'] as Record<string, unknown>;
      if ('total' in scoredObj && typeof scoredObj['total'] === 'number') scored = scoredObj['total'];
    }

    if ('total' in penaltyObj && typeof penaltyObj['total'] === 'number') total = penaltyObj['total'];

    return { label, total: `${scored} (${total})` };
  }

  private extractBreakdownValue(value: unknown): Omit<StatBreakdown, 'label'> {
    if (!value || typeof value !== 'object') {
      return { total: this.formatValue(value) };
    }

    const obj = value as Record<string, unknown>;
    const result: Omit<StatBreakdown, 'label'> = {};

    if ('home' in obj && 'away' in obj && 'total' in obj) {
      if (typeof obj['home'] === 'number') result.home = String(obj['home']);
      if (typeof obj['away'] === 'number') result.away = String(obj['away']);
      const total = obj['total'];
      if (typeof total === 'number') result.total = String(total);
      return result;
    }

    if ('played' in obj && typeof obj['played'] === 'object' && obj['played'] !== null) {
      const played = obj['played'] as Record<string, unknown>;
      if ('home' in played && 'away' in played && 'total' in played) {
        if (typeof played['home'] === 'number') result.home = String(played['home']);
        if (typeof played['away'] === 'number') result.away = String(played['away']);
        if (typeof played['total'] === 'number') result.total = String(played['total']);
        return result;
      }
    }

    if ('total' in obj && typeof obj['total'] === 'object' && obj['total'] !== null) {
      const total = obj['total'] as Record<string, unknown>;
      if ('home' in total && 'away' in total && 'total' in total) {
        if (typeof total['home'] === 'number') result.home = String(total['home']);
        if (typeof total['away'] === 'number') result.away = String(total['away']);
        if (typeof total['total'] === 'number') result.total = String(total['total']);
        return result;
      }
    }

    return { total: this.formatValue(value) };
  }
}
