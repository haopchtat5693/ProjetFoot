import { CommonModule } from '@angular/common';
import { Component, computed, effect, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import type { DetailHighlight } from '../../interfaces/detail';
import type { Fixture } from '../../interfaces/dashboard';
import { catchError, of } from 'rxjs';
import { toNumberOrNull } from '../../utils';
import { createDetailHighlight, createRouteEntitySignal, sortByIdDesc } from '../../utils';

@Component({
  selector: 'app-league-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './league-detail.html',
  styleUrl: './league-detail.scss',
})
export class LeagueDetail {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected readonly selectedSeasonId = signal<number | null>(null);
  protected readonly leagueFixtures = signal<Fixture[]>([]);

  protected readonly league = createRouteEntitySignal(this.route, 'leagueId', (leagueId) =>
    this.svc.getLeagueById(leagueId),
  );

  protected readonly highlights = computed<DetailHighlight[]>(() => {
    const league = this.league();
    if (!league) return [];

    return [
      createDetailHighlight('ID', league.id),
      createDetailHighlight('Country', league.country),
      createDetailHighlight('Type', league.league_type),
      createDetailHighlight('Seasons', league.seasons?.length ?? 0),
    ];
  });

  protected readonly sortedSeasons = computed(() => {
    const seasons = this.league()?.seasons ?? [];
    return sortByIdDesc(seasons);
  });

  constructor() {
    effect(() => {
      const league = this.league();
      this.selectedSeasonId.set(null);
      this.leagueFixtures.set([]);

      if (!league) return;

      const firstSeason = league.seasons?.[0];
      if (firstSeason) {
        this.selectedSeasonId.set(firstSeason.id);
      }
    });

    effect((onCleanup) => {
      const league = this.league();
      const seasonId = this.selectedSeasonId();

      this.leagueFixtures.set([]);

      if (!league || seasonId === null) return;

      console.log('[LeagueDetail] Fetching fixtures for league:', league.id, 'season:', seasonId);
      const fixturesSubscription = this.svc
        .getFixturesByLeague(league.id, seasonId)
        .pipe(
          catchError((error) => {
            console.error('[LeagueDetail] Error fetching fixtures:', error);
            return of([] as Fixture[]);
          })
        )
        .subscribe((fixtures) => {
          console.log('[LeagueDetail] Fixtures received:', fixtures.length, 'fixtures', fixtures);
          this.leagueFixtures.set(fixtures);
        });

      onCleanup(() => fixturesSubscription.unsubscribe());
    });
  }

  protected onSeasonChange(seasonId: number | string | null): void {
    this.selectedSeasonId.set(toNumberOrNull(seasonId));
  }
}