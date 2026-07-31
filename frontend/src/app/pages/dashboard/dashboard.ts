import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { catchError, forkJoin, of } from 'rxjs';
import { DashboardService } from '../../services/dashboard.service';
import type {
  Team,
  Season,
  Player,
  PlayerSeasonStats,
  PlayerWithSeasonStats,
} from '../../interfaces/dashboard';
import { toSignal } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard {
  private readonly svc = inject(DashboardService);

  protected entities = [
    { label: 'Teams', value: 'teams' },
    { label: 'Players', value: 'players' },
  ];

  protected selectedEntity = signal('teams');

  protected teams = toSignal(this.svc.getTeams(), { initialValue: [] as Team[] });
  protected seasons = toSignal(this.svc.getSeasons(), { initialValue: [] as Season[] });

  protected selectedTeamId = signal<number | null>(null);
  protected selectedSeasonId = signal<number | null>(null);
  protected selectedPlayerId = signal<number | null>(null);
  protected availablePlayers = signal<Player[]>([]);
  protected playerSearchName = signal('');

  protected playerStats = signal<PlayerWithSeasonStats[]>([]);

  protected onTeamChange(teamId: number | string | null): void {
    this.selectedTeamId.set(this.toNumberOrNull(teamId));
    this.loadAvailablePlayers();
  }

  protected onSeasonChange(seasonId: number | string | null): void {
    this.selectedSeasonId.set(this.toNumberOrNull(seasonId));
    this.loadAvailablePlayers();
  }

  protected onPlayerChange(playerId: number | string | null): void {
    this.selectedPlayerId.set(this.toNumberOrNull(playerId));
  }

  protected onSearchPlayers(): void {
    const searchTerm = this.playerSearchName().trim();
    if (!searchTerm) {
      this.loadAvailablePlayers();
      return;
    }

    this.selectedEntity.set('players');
    this.playerStats.set([]);

    this.svc
      .searchPlayersByName(searchTerm)
      .pipe(
        catchError(() => {
          console.warn(`Impossible de rechercher le joueur "${searchTerm}".`);
          return of([] as Player[]);
        }),
      )
      .subscribe((players) => {
        this.availablePlayers.set(players);
        this.playerStats.set(
          players.map((player) => ({
            player,
            stats: {
              id: -1,
              player_id: player.id,
              season_id: this.selectedSeasonId() ?? -1,
              total_goals: null,
              total_assists: null,
              total_minutes: null,
              avg_rating: null,
            } as PlayerSeasonStats,
          })),
        );
        this.selectedPlayerId.set(players.length ? players[0].id : null);
      });
  }

  private toNumberOrNull(value: number | string | null): number | null {
    if (value === null || value === '') return null;
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : null;
  }

  private loadAvailablePlayers(): void {
    const teamId = this.selectedTeamId();
    const seasonId = this.selectedSeasonId();

    this.playerStats.set([]);

    if (!teamId || !seasonId) {
      this.availablePlayers.set([]);
      this.selectedPlayerId.set(null);
      return;
    }

    this.svc
      .getTeamPlayersForSeason(teamId, seasonId)
      .pipe(
        catchError(() => {
          console.warn('Impossible de charger la liste des joueurs pour cette equipe/saison.');
          return of([] as Player[]);
        }),
      )
      .subscribe((players) => {
        this.availablePlayers.set(players);

        const selectedPlayerId = this.selectedPlayerId();
        const selectedStillAvailable =
          selectedPlayerId !== null && players.some((player) => player.id === selectedPlayerId);

        if (!selectedStillAvailable) {
          this.selectedPlayerId.set(players.length ? players[0].id : null);
        }
      });
  }

  protected onFetchPlayerStats(): void {
    const seasonId = this.selectedSeasonId();
    const playerId = this.selectedPlayerId();

    if (!seasonId || !playerId) return;

    this.selectedEntity.set('players');

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
            },
          });
        }),
      )
      .subscribe(({ player, stats }) => {
        this.playerStats.set([{ player, stats }]);
      });
  }
}
