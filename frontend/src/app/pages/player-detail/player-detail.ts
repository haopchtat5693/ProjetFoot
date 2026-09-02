import { CommonModule } from '@angular/common';
import { Component, computed, effect, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { catchError, combineLatest, of, switchMap } from 'rxjs';
import { ApiService } from '../../services/api.service';
import type { PlayerSeasonStats, Season } from '../../interfaces/tables';
import type { DetailHighlight } from '../../interfaces/detail';
import { createDetailHighlight, createRouteEntitySignal, sortByIdDesc } from '../../utils';
import { toNumberOrNull } from '../../utils';

@Component({
  selector: 'app-player-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './player-detail.html',
  styleUrl: './player-detail.scss',
})
export class PlayerDetail {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected readonly seasons = toSignal(this.svc.getSeasons(), { initialValue: [] as Season[] });
  protected readonly selectedSeasonId = signal<number | null>(null);
  protected readonly player = createRouteEntitySignal(this.route, 'playerId', (playerId) =>
    this.svc.getPlayerById(playerId),
  );

  protected readonly playerSeasonStats = toSignal(
    combineLatest([toObservable(this.player), toObservable(this.selectedSeasonId)]).pipe(
      switchMap(([player, seasonId]) => {
        if (!player || seasonId === null) {
          return of(null as PlayerSeasonStats | null);
        }

        return this.svc.getPlayerSeasonStats(player.id, seasonId).pipe(
          catchError(() => {
            console.warn(`Impossible de charger les stats du joueur ${player.id} pour la saison ${seasonId}.`);
            return of(null as PlayerSeasonStats | null);
          }),
        );
      }),
    ),
    { initialValue: null as PlayerSeasonStats | null },
  );

  protected readonly seasonOptions = computed(() => sortByIdDesc(this.seasons()));

  protected readonly highlights = computed<DetailHighlight[]>(() => {
    const player = this.player();
    if (!player) return [];

    return [
      createDetailHighlight('ID', player.id),
      createDetailHighlight('Nationality', player.nationality),
      createDetailHighlight('Position', player.position),
      createDetailHighlight('Age', player.age),
    ];
  });

  protected readonly statHighlights = computed<DetailHighlight[]>(() => {
    const stats = this.playerSeasonStats();

    if (!stats) {
      return [];
    }

    return [
      createDetailHighlight('Season', `#${stats.season_id}`),
      createDetailHighlight('Goals', stats.total_goals),
      createDetailHighlight('Assists', stats.total_assists),
      createDetailHighlight('Minutes', stats.total_minutes),
      createDetailHighlight('Avg rating', stats.avg_rating),
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

      const seasonExists = selectedSeasonId !== null && seasons.some((season: Season) => season.id === selectedSeasonId);

      if (!seasonExists) {
        this.selectedSeasonId.set(seasons[0]?.id ?? null);
      }
    });
  }

  protected onSeasonChange(seasonId: number | string | null): void {
    const parsedSeasonId = toNumberOrNull(seasonId);
    this.selectedSeasonId.set(parsedSeasonId);
  }

}