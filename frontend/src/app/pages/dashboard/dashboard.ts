import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { forkJoin, map, of, switchMap } from 'rxjs';
import { DashboardService } from '../../services/dashboard.service';
import type { Team, Season, Player, PlayerWithSeasonStats } from '../../interfaces/dashboard';

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

  protected selectedEntity = 'teams';

  protected teams: Team[] = [];
  protected seasons: Season[] = [];

  protected selectedTeamId: number | null = null;
  protected selectedSeasonId: number | null = null;

  protected playerStats: PlayerWithSeasonStats[] = [];

  constructor() {
    this.loadInitialData();
  }

  private loadInitialData(): void {
    this.svc.getTeams().subscribe((res: Team[]) => (this.teams = res || []));
    this.svc.getSeasons().subscribe((res: Season[]) => (this.seasons = res || []));
  }

  protected onFetchPlayers(): void {
    if (!this.selectedTeamId || !this.selectedSeasonId) return;

    this.selectedEntity = 'players';
    
    this.svc
      .getTeamPlayersForSeason(this.selectedTeamId, this.selectedSeasonId)
      .pipe(
        switchMap((players: Player[]) =>
          players.length
            ? forkJoin(
                players.map((player) =>
                  this.svc.getPlayerSeasonStats(player.id, this.selectedSeasonId as number),
                ),
              ).pipe(
                map((stats) =>
                  players.map((player, index) => ({ player, stats: stats[index] })),
                ),
              )
            : of([]),
        ),
      )
      .subscribe((res) => (this.playerStats = res || []));
  }
}
