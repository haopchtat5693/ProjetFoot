import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, map, of, startWith, switchMap } from 'rxjs';
import { DashboardService } from '../../services/dashboard.service';
import type { League } from '../../interfaces/dashboard';

@Component({
  selector: 'app-league-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './league-detail.html',
  styleUrl: './league-detail.scss',
})
export class LeagueDetail {
  private readonly svc = inject(DashboardService);
  private readonly route = inject(ActivatedRoute);

  protected readonly league = toSignal<League | null>(
    this.route.paramMap.pipe(
      map((params) => params.get('leagueId')),
      switchMap((rawLeagueId) => {
        const leagueId = Number(rawLeagueId);
        return rawLeagueId && Number.isFinite(leagueId) ? this.svc.getLeagueById(leagueId) : of(null as League | null);
      }),
      startWith(null as League | null),
      catchError(() => of(null as League | null)),
    ),
    { requireSync: true },
  );

  protected readonly highlights = computed(() => {
    const league = this.league();
    if (!league) return [] as { label: string; value: string }[];

    return [
      { label: 'ID', value: String(league.id) },
      { label: 'Country', value: league.country || 'Unknown' },
      { label: 'Type', value: league.league_type || 'Unknown' },
      { label: 'Seasons', value: String(league.seasons?.length ?? 0) },
    ];
  });

  protected readonly sortedSeasons = computed(() => {
    const seasons = this.league()?.seasons ?? [];
    return [...seasons].sort((left, right) => right.id - left.id);
  });
}