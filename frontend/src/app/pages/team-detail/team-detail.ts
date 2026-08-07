import { CommonModule } from '@angular/common';
import { Component, computed, effect, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import type { League, Player, Season, TeamSeasonStats } from '../../interfaces/dashboard';
import type { DetailHighlight } from '../../interfaces/detail';
import { catchError, of } from 'rxjs';
import { toNumberOrNull } from '../../utils';
import { createDetailHighlight, createRouteEntitySignal, formatDetailValue, sortByIdDesc } from '../../utils';

@Component({
  selector: 'app-team-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './team-detail.html',
  styleUrl: './team-detail.scss',
})
export class TeamDetail {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected readonly leagues = signal<League[]>([]);
  protected readonly selectedLeagueId = signal<number | null>(null);
  protected readonly selectedSeasonId = signal<number | null>(null);
  protected readonly teamSeasonStats = signal<TeamSeasonStats | null>(null);
  protected readonly teamPlayers = signal<Player[]>([]);

  protected readonly team = createRouteEntitySignal(this.route, 'teamId', (teamId) =>
    this.svc.getTeamById(teamId),
  );

  protected readonly selectedLeague = computed(() => {
    const leagueId = this.selectedLeagueId();

    if (leagueId === null) return null;

    return this.leagues().find((league) => league.id === leagueId) ?? null;
  });

  protected readonly availableSeasons = computed(() => {
    const seasons = this.selectedLeague()?.seasons ?? [];
    return sortByIdDesc(seasons);
  });

  protected readonly selectedSeason = computed(() => {
    const seasonId = this.selectedSeasonId();

    if (seasonId === null) return null;

    return this.availableSeasons().find((season) => season.id === seasonId) ?? null;
  });

  protected readonly highlights = computed<DetailHighlight[]>(() => {
    const team = this.team();
    if (!team) return [];

    return [
      createDetailHighlight('ID', team.id),
      createDetailHighlight('Country', team.country),
      createDetailHighlight('City', team.city),
      createDetailHighlight('Coach', team.coach_id ? `#${team.coach_id}` : 'Not linked'),
    ];
  });

  protected readonly statHighlights = computed<DetailHighlight[]>(() => {
    const stats = this.teamSeasonStats();

    if (!stats) {
      return [];
    }

    return [
      createDetailHighlight('League', this.selectedLeague()?.name ?? `#${stats.league_id}`),
      createDetailHighlight('Season', `#${stats.season_id}`),
      createDetailHighlight('Fixtures', formatDetailValue(stats.fixtures)),
      createDetailHighlight('Goals', formatDetailValue(stats.goals)),
      createDetailHighlight('Clean sheet', formatDetailValue(stats.clean_sheet)),
      createDetailHighlight('Failed to score', formatDetailValue(stats.failed_to_score)),
      createDetailHighlight('Penalty', formatDetailValue(stats.penalty)),
      createDetailHighlight('Cards', formatDetailValue(stats.cards)),
    ];
  });

  constructor() {
    effect((onCleanup) => {
      const team = this.team();

      this.leagues.set([]);
      this.selectedLeagueId.set(null);
      this.selectedSeasonId.set(null);
      this.teamSeasonStats.set(null);
      this.teamPlayers.set([]);

      if (!team) {
        return;
      }

      const subscription = this.svc
        .lookupLeagues({ team: team.id })
        .pipe(
          catchError(() => {
            console.warn(`Impossible de charger les ligues pour l'equipe ${team.id}.`);
            return of([] as League[]);
          }),
        )
        .subscribe((leagues) => {
          this.leagues.set(leagues);

          const preferredLeague = leagues[0] ?? null;
          this.selectedLeagueId.set(preferredLeague?.id ?? null);
          this.selectedSeasonId.set(this.pickSeasonId(preferredLeague?.seasons));
        });

      onCleanup(() => subscription.unsubscribe());
    });

    effect((onCleanup) => {
      const team = this.team();
      const leagueId = this.selectedLeagueId();
      const seasonId = this.selectedSeasonId();

      this.teamSeasonStats.set(null);
      this.teamPlayers.set([]);

      if (!team || leagueId === null || seasonId === null) {
        return;
      }

      const subscription = this.svc
        .getTeamSeasonStats(team.id, leagueId, seasonId)
        .pipe(
          catchError(() => {
            console.warn(`Impossible de charger les stats equipe pour team=${team.id}, league=${leagueId}, season=${seasonId}.`);
            return of(null as TeamSeasonStats | null);
          }),
        )
        .subscribe((stats) => {
          this.teamSeasonStats.set(stats);
        });

      const playersSubscription = this.svc
        .getTeamPlayersForSeason(team.id, seasonId)
        .pipe(
          catchError(() => {
            console.warn(`Impossible de charger les joueurs pour team=${team.id}, season=${seasonId}.`);
            return of([] as Player[]);
          }),
        )
        .subscribe((players) => {
          this.teamPlayers.set(players);
        });

      onCleanup(() => {
        subscription.unsubscribe();
        playersSubscription.unsubscribe();
      });
    });
  }

  protected onLeagueChange(leagueId: number | string | null): void {
    const parsedLeagueId = toNumberOrNull(leagueId);
    this.selectedLeagueId.set(parsedLeagueId);

    if (parsedLeagueId === null) {
      this.selectedSeasonId.set(null);
      return;
    }

    const matchedLeague = this.leagues().find((league) => league.id === parsedLeagueId) ?? null;
    this.selectedSeasonId.set(this.pickSeasonId(matchedLeague?.seasons));
  }

  protected onSeasonChange(seasonId: number | string | null): void {
    this.selectedSeasonId.set(toNumberOrNull(seasonId));
  }

  protected formatValue(value: unknown): string {
    if (value === null || value === undefined || value === '') {
      return '—';
    }

    if (Array.isArray(value)) {
      return value.length ? `${value.length}` : '—';
    }

    if (typeof value === 'object') {
      return Object.entries(value as Record<string, unknown>)
        .map(([key, nestedValue]) => `${key}: ${this.formatValue(nestedValue)}`)
        .join(' · ');
    }

    return String(value);
  }

  protected squadLabel(player: Player): string {
    return [player.position, player.age ? `${player.age}y` : null].filter(Boolean).join(' · ') || 'No extra info';
  }

  private pickSeasonId(seasons: Season[] | undefined | null): number | null {
    if (!seasons?.length) return null;

    return seasons[0]?.id ?? null;
  }

}
