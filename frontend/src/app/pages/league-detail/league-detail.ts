import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import type { DetailHighlight } from '../../interfaces/detail';
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
}