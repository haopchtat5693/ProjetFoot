import { CommonModule } from '@angular/common';
import { Component, computed, effect, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { TeamDetailService, type StatBreakdown } from '../../services/team-detail.service';
import type { League, Player, Season, TeamSeasonStats } from '../../interfaces/dashboard';
import type { DetailHighlight } from '../../interfaces/detail';
import { catchError, of } from 'rxjs';
import { toNumberOrNull } from '../../utils';
import { createDetailHighlight, createRouteEntitySignal, sortByIdDesc } from '../../utils';

@Component({
  selector: 'app-team-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './team-detail.html',
  styleUrl: './team-detail.scss',
})
export class TeamDetail {
  private readonly api = inject(ApiService);
  private readonly detailSvc = inject(TeamDetailService);
  private readonly route = inject(ActivatedRoute);

  protected readonly leagues = signal<League[]>([]);
  protected readonly selectedLeagueId = signal<number | null>(null);
  protected readonly selectedSeasonId = signal<number | null>(null);
  protected readonly teamSeasonStats = signal<TeamSeasonStats | null>(null);
  protected readonly teamPlayers = signal<Player[]>([]);

  protected readonly team = createRouteEntitySignal(this.route, 'teamId', (teamId) =>
    this.api.getTeamById(teamId),
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

  protected readonly highlights = computed<DetailHighlight[]>(() => {
    const team = this.team();
    if (!team) return [];
    return [
      createDetailHighlight('ID', team.id),
      createDetailHighlight('Country', team.country),
      createDetailHighlight('City', team.city),
    ];
  });

  protected readonly statHighlights = computed<DetailHighlight[]>(() => {
    const stats = this.teamSeasonStats();
    if (!stats) return [];
    return [
      createDetailHighlight('League', this.selectedLeague()?.name ?? `#${stats.league_id}`),
      createDetailHighlight('Season', `#${stats.season_id}`),
    ];
  });

  protected readonly statBreakdowns = computed<StatBreakdown[]>(() => {
    const stats = this.teamSeasonStats();
    if (!stats) return [];
    return [
      this.detailSvc.createBreakdown('Fixtures', stats.fixtures),
      this.detailSvc.createBreakdown('Goals (For)', stats.goals?.['for']),
      this.detailSvc.createBreakdown('Goals (Against)', stats.goals?.['against']),
      this.detailSvc.createBreakdown('Clean Sheet', stats.clean_sheet),
      this.detailSvc.createBreakdown('Failed to Score', stats.failed_to_score),
      this.detailSvc.createSimplePenaltyBreakdown('Penalties (Total)', stats.penalty),
      this.detailSvc.createCardBreakdown('Yellow Cards', stats.cards, 'yellow'),
      this.detailSvc.createCardBreakdown('Red Cards', stats.cards, 'red'),
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

      if (!team) return;

      const subscription = this.api
        .lookupLeagues({ team: team.id })
        .pipe(catchError(() => of([] as League[])))
        .subscribe((leagues) => {
          this.leagues.set(leagues);
          const preferredLeague = leagues[0] ?? null;
          this.selectedLeagueId.set(preferredLeague?.id ?? null);
          this.selectedSeasonId.set(this.getFirstSeasonId(preferredLeague?.seasons));
        });

      onCleanup(() => subscription.unsubscribe());
    });

    effect((onCleanup) => {
      const team = this.team();
      const leagueId = this.selectedLeagueId();
      const seasonId = this.selectedSeasonId();

      this.teamSeasonStats.set(null);
      this.teamPlayers.set([]);

      if (!team || leagueId === null || seasonId === null) return;

      const statsSubscription = this.api
        .getTeamSeasonStats(team.id, leagueId, seasonId)
        .pipe(catchError(() => of(null as TeamSeasonStats | null)))
        .subscribe((stats) => this.teamSeasonStats.set(stats));

      const playersSubscription = this.api
        .getTeamPlayersForSeason(team.id, seasonId)
        .pipe(catchError(() => of([] as Player[])))
        .subscribe((players) => this.teamPlayers.set(players));

      onCleanup(() => {
        statsSubscription.unsubscribe();
        playersSubscription.unsubscribe();
      });
    });
  }

  protected onLeagueChange(leagueId: number | string | null): void {
    const parsed = toNumberOrNull(leagueId);
    this.selectedLeagueId.set(parsed);

    if (parsed === null) {
      this.selectedSeasonId.set(null);
      return;
    }

    const league = this.leagues().find((l) => l.id === parsed) ?? null;
    this.selectedSeasonId.set(this.getFirstSeasonId(league?.seasons));
  }

  protected onSeasonChange(seasonId: number | string | null): void {
    this.selectedSeasonId.set(toNumberOrNull(seasonId));
  }

  protected squadLabel(player: Player): string {
    return [player.position, player.age ? `${player.age}y` : null].filter(Boolean).join(' · ') || 'No extra info';
  }

  private getFirstSeasonId(seasons: Season[] | undefined | null): number | null {
    return seasons?.length ? seasons[0]?.id ?? null : null;
  }
}

