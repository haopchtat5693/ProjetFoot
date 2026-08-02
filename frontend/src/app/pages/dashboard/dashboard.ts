import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, forkJoin, of } from 'rxjs';
import { PlayerLookupCardComponent } from '../../components/player-lookup-card-component/player-lookup-card.component';
import { TeamLeagueLookupCardComponent } from '../../components/team-league-lookup-card-component/team-league-lookup-card.component';
import { DashboardService } from '../../services/dashboard.service';
import type {
  League,
  Player,
  PlayerSeasonStats,
  PlayerWithSeasonStats,
  Season,
  Team,
  TeamSeasonStats,
} from '../../interfaces/dashboard';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, TeamLeagueLookupCardComponent, PlayerLookupCardComponent],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard {
  private readonly svc = inject(DashboardService);

  protected teams = toSignal(this.svc.getTeams(), { initialValue: [] as Team[] });
  protected seasons = toSignal(this.svc.getSeasons(), { initialValue: [] as Season[] });
  protected teamResults = signal<Team[]>([]);
  protected leagueResults = signal<League[]>([]);
  protected teamPlayers = signal<Player[]>([]);
  protected teamStats = signal<TeamSeasonStats | null>(null);
  protected playerResults = signal<Player[]>([]);
  protected playerStats = signal<PlayerWithSeasonStats[]>([]);

  protected selectedTeamId = signal<number | null>(null);
  protected selectedLeagueId = signal<number | null>(null);
  protected selectedSeasonId = signal<number | null>(null);
  protected selectedPlayerId = signal<number | null>(null);
  protected selectedPlayerSeasonId = signal<number | null>(null);

  protected playerSearchName = signal('');
  protected teamSearchName = signal('');
  protected leagueSearchName = signal('');

  protected selectedLeague = computed(() => {
    const leagueId = this.selectedLeagueId();

    if (leagueId === null) return null;

    return this.leagueResults().find((league) => league.id === leagueId) ?? null;
  });

  protected selectedTeam = computed(() => {
    const teamId = this.selectedTeamId();

    if (teamId === null) return null;

    return this.teamResults().find((team) => team.id === teamId) ?? this.teams().find((team) => team.id === teamId) ?? null;
  });

  protected selectedSeason = computed(() => {
    const seasonId = this.selectedSeasonId();

    if (seasonId === null) return null;

    return this.selectedLeague()?.seasons?.find((season) => season.id === seasonId) ?? null;
  });

  protected availableSeasons = computed(() => this.selectedLeague()?.seasons ?? []);

  protected onSearchTeams(): void {
    const searchTerm = this.teamSearchName().trim();

    this.clearTeamSelections();

    if (!searchTerm) {
      this.teamResults.set([]);
      return;
    }

    this.svc
      .searchTeamsByName(searchTerm)
      .pipe(
        catchError(() => {
          console.warn(`Impossible de rechercher l'equipe "${searchTerm}".`);
          return of([] as Team[]);
        }),
      )
      .subscribe((teams) => {
        this.teamResults.set(teams);
        this.selectedTeamId.set(teams.length ? teams[0].id : null);

        if (teams.length) {
          this.loadLeaguesForSelection();
        } else {
          this.clearTeamSelections();
        }
      });
  }

  protected onTeamChange(teamId: number | string | null): void {
    const parsedTeamId = this.toNumberOrNull(teamId);
    this.selectedTeamId.set(parsedTeamId);

    if (parsedTeamId === null) {
      this.clearTeamSelections();
      return;
    }

    this.loadLeaguesForSelection();
  }

  protected onLeagueChange(leagueId: number | string | null): void {
    const parsedLeagueId = this.toNumberOrNull(leagueId);
    this.selectedLeagueId.set(parsedLeagueId);

    if (parsedLeagueId === null) {
      this.selectedSeasonId.set(null);
      this.teamStats.set(null);
      this.teamPlayers.set([]);
      return;
    }

    const matchedLeague = this.leagueResults().find((league) => league.id === parsedLeagueId);
    this.selectedSeasonId.set(this.pickSeasonId(matchedLeague?.seasons));
    this.loadTeamInsights();
  }

  protected onSeasonChange(seasonId: number | string | null): void {
    this.selectedSeasonId.set(this.toNumberOrNull(seasonId));
    this.loadTeamInsights();
  }

  protected onPlayerChange(playerId: number | string | null): void {
    this.selectedPlayerId.set(this.toNumberOrNull(playerId));
  }

  protected onPlayerSeasonChange(seasonId: number | string | null): void {
    this.selectedPlayerSeasonId.set(this.toNumberOrNull(seasonId));
  }

  protected onSearchPlayers(): void {
    const searchTerm = this.playerSearchName().trim();

    if (!searchTerm) {
      this.playerResults.set([]);
      this.selectedPlayerId.set(null);
      return;
    }

    this.playerStats.set([]);
    this.playerResults.set([]);

    this.svc
      .searchPlayersByName(searchTerm)
      .pipe(
        catchError(() => {
          console.warn(`Impossible de rechercher le joueur "${searchTerm}".`);
          return of([] as Player[]);
        }),
      )
      .subscribe((players) => {
        this.playerResults.set(players);
        this.selectedPlayerId.set(players.length ? players[0].id : null);
      });
  }

  protected onFetchPlayerStats(): void {
    const seasonId = this.selectedPlayerSeasonId();
    const playerId = this.selectedPlayerId();

    if (seasonId === null || playerId === null) return;

    forkJoin({
      player: this.svc.getPlayerById(playerId),
      stats: this.svc.getPlayerSeasonStats(playerId, seasonId),
    })
      .pipe(
        catchError(() => {
          console.warn(`Impossible de charger joueur/stats pour player=${playerId}, season=${seasonId}.`);
          return of({
            player: {
              id: playerId,
              name: `Player #${playerId}`,
              position: null,
              age: null,
              photo: null,
            } as Player,
            stats: {
              id: -1,
              player_id: playerId,
              season_id: seasonId,
              total_goals: null,
              total_assists: null,
              total_minutes: null,
              avg_rating: null,
            } as PlayerSeasonStats,
          });
        }),
      )
      .subscribe(({ player, stats }) => {
        this.playerStats.set([{ player, stats }]);
      });
  }

  protected statEntries(value: Record<string, unknown> | null | undefined): { key: string; value: string }[] {
    if (!value) return [];

    return Object.entries(value).map(([key, rawValue]) => ({
      key,
      value: this.formatValue(rawValue),
    }));
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

  private toNumberOrNull(value: number | string | null): number | null {
    if (value === null || value === '') return null;

    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : null;
  }

  private pickSeasonId(seasons: Season[] | undefined | null): number | null {
    if (!seasons?.length) return null;

    return seasons[0]?.id ?? null;
  }

  private clearTeamSelections(): void {
    this.leagueResults.set([]);
    this.selectedLeagueId.set(null);
    this.selectedSeasonId.set(null);
    this.teamStats.set(null);
    this.teamPlayers.set([]);
  }

  protected onSearchLeagues(): void {
    const searchTerm = this.leagueSearchName().trim();
    this.loadLeaguesForSelection(searchTerm || undefined);
  }

  private loadLeaguesForSelection(search?: string): void {
    const query = {
      search: search ?? (this.leagueSearchName().trim() || undefined),
    };

    this.leagueResults.set([]);
    this.selectedLeagueId.set(null);
    this.selectedSeasonId.set(null);
    this.teamStats.set(null);
    this.teamPlayers.set([]);

    this.svc
      .lookupLeagues(query)
      .pipe(
        catchError(() => {
          console.warn('Impossible de charger les ligues pour la selection courante.');
          return of([] as League[]);
        }),
      )
      .subscribe((leagues) => {
        this.leagueResults.set(leagues);

        const preferredLeague = leagues[0] ?? null;
        this.selectedLeagueId.set(preferredLeague?.id ?? null);
        this.selectedSeasonId.set(this.pickSeasonId(preferredLeague?.seasons));

        this.loadTeamInsights();
      });
  }

  private loadTeamInsights(): void {
    const teamId = this.selectedTeamId();
    const leagueId = this.selectedLeagueId();
    const seasonId = this.selectedSeasonId();

    this.teamStats.set(null);
    this.teamPlayers.set([]);

    if (teamId === null || leagueId === null || seasonId === null) {
      return;
    }

    forkJoin({
      stats: this.svc.getTeamSeasonStats(teamId, leagueId, seasonId).pipe(
        catchError(() => {
          console.warn('Impossible de charger les stats de l\'equipe pour cette ligue/saison.');
          return of(null as TeamSeasonStats | null);
        }),
      ),
      players: this.svc.getTeamPlayersForSeason(teamId, seasonId).pipe(
        catchError(() => {
          console.warn('Impossible de charger la liste des joueurs pour cette equipe/saison.');
          return of([] as Player[]);
        }),
      ),
    }).subscribe(({ stats, players }) => {
      this.teamStats.set(stats);
      this.teamPlayers.set(players);
    });
  }
}
