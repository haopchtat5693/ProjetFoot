import { type Signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute } from '@angular/router';
import { catchError, map, type Observable, of, startWith, switchMap } from 'rxjs';
import { UNKNOWN_TEXT } from '../constants/display';
import type { DetailHighlight } from '../interfaces/detail';

export function createRouteEntitySignal<T>(
  route: ActivatedRoute,
  paramName: string,
  loadById: (id: number) => Observable<T>,
): Signal<T | null> {
  return toSignal<T | null>(
    route.paramMap.pipe(
      map((params) => params.get(paramName)),
      switchMap((rawId) => {
        const parsedId = Number(rawId);
        return rawId && Number.isFinite(parsedId) ? loadById(parsedId) : of(null as T | null);
      }),
      startWith(null as T | null),
      catchError(() => of(null as T | null)),
    ),
    { requireSync: true },
  );
}

export function sortByIdDesc<T extends { id: number }>(items: readonly T[]): T[] {
  return [...items].sort((left, right) => right.id - left.id);
}

export function formatDetailValue(value: unknown, fallback = UNKNOWN_TEXT): string {
  if (value === null || value === undefined || value === '') {
    return fallback;
  }

  return String(value);
}

export function createDetailHighlight(
  label: string,
  value: unknown,
  fallback = UNKNOWN_TEXT,
): DetailHighlight {
  return {
    label,
    value: formatDetailValue(value, fallback),
  };
}