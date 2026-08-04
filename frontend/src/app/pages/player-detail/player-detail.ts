import { CommonModule } from '@angular/common';
import { Component, computed, effect, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, map, of, startWith, switchMap } from 'rxjs';
import { DashboardService } from '../../services/dashboard.service';
import type { Player, PlayerSeasonStats, Season } from '../../interfaces/dashboard';
import { toNumberOrNull } from '../../utils';

@Component({
  selector: 'app-player-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './player-detail.html',
  styleUrl: './player-detail.scss',
})
export class PlayerDetail {
  private readonly svc = inject(DashboardService);
  private readonly route = inject(ActivatedRoute);

  protected readonly seasons = toSignal(this.svc.getSeasons(), { initialValue: [] as Season[] });
  protected readonly selectedSeasonId = signal<number | null>(null);
  protected readonly playerSeasonStats = signal<PlayerSeasonStats | null>(null);

  protected readonly player = toSignal<Player | null>(
    this.route.paramMap.pipe(
      map((params) => params.get('playerId')),
      switchMap((rawPlayerId) => {
        const playerId = Number(rawPlayerId);
        return rawPlayerId && Number.isFinite(playerId) ? this.svc.getPlayerById(playerId) : of(null as Player | null);
      }),
      startWith(null as Player | null),
      catchError(() => of(null as Player | null)),
    ),
    { requireSync: true },
  );

  protected readonly seasonOptions = computed(() => [...this.seasons()].sort((left, right) => right.id - left.id));

  protected readonly highlights = computed(() => {
    const player = this.player();
    if (!player) return [] as { label: string; value: string }[];

    return [
      { label: 'ID', value: String(player.id) },
      { label: 'Nationality', value: player.nationality || 'Unknown' },
      { label: 'Position', value: player.position || 'Unknown' },
      { label: 'Age', value: player.age ? String(player.age) : 'Unknown' },
    ];
  });

  protected readonly statHighlights = computed(() => {
    const stats = this.playerSeasonStats();

    if (!stats) {
      return [] as { label: string; value: string }[];
    }

    return [
      { label: 'Season', value: `#${stats.season_id}` },
      { label: 'Goals', value: this.formatStatValue(stats.total_goals) },
      { label: 'Assists', value: this.formatStatValue(stats.total_assists) },
      { label: 'Minutes', value: this.formatStatValue(stats.total_minutes) },
      { label: 'Avg rating', value: this.formatStatValue(stats.avg_rating) },
    ];
  });

  constructor() {
    effect(() => {
      const seasons = this.seasonOptions();
      const selectedSeasonId = this.selectedSeasonId();

      if (!seasons.length) {
        if (selectedSeasonId !== null) {
          this.selectedSeasonId.set(null);
        }

        return;
      }

      const seasonExists = selectedSeasonId !== null && seasons.some((season) => season.id === selectedSeasonId);

      if (!seasonExists) {
        this.selectedSeasonId.set(seasons[0]?.id ?? null);
      }
    });

    effect((onCleanup) => {
      const player = this.player();
      const seasonId = this.selectedSeasonId();

      this.playerSeasonStats.set(null);

      if (!player || seasonId === null) {
        return;
      }

      const subscription = this.svc
        .getPlayerSeasonStats(player.id, seasonId)
        .pipe(
          catchError(() => {
            console.warn(`Impossible de charger les stats du joueur ${player.id} pour la saison ${seasonId}.`);
            return of(null as PlayerSeasonStats | null);
          }),
        )
        .subscribe((stats) => {
          this.playerSeasonStats.set(stats);
        });

      onCleanup(() => subscription.unsubscribe());
    });
  }

  protected onSeasonChange(seasonId: number | string | null): void {
    const parsedSeasonId = toNumberOrNull(seasonId);
    this.selectedSeasonId.set(parsedSeasonId);
  }

  private formatStatValue(value: number | string | null | undefined): string {
    if (value === null || value === undefined || value === '') {
      return 'Unknown';
    }

    return String(value);
  }

}