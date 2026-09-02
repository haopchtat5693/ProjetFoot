import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, map, of, switchMap } from 'rxjs';
import { ApiService } from '../../services/api.service';
import { SearchResultsService } from '../../services/search-results.service';
import type { SearchResult, SearchScope } from '../../interfaces/search-results';
import type { League, Player, Stadium, Team, Coach } from '../../interfaces/tables';

@Component({
  selector: 'app-search-results',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './search-results.html',
  styleUrl: './search-results.scss',
})
export class SearchResults {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly searchResultsService = inject(SearchResultsService);

  protected readonly queryParamMap = toSignal(this.route.queryParamMap, {
    initialValue: this.route.snapshot.queryParamMap,
  });

  protected readonly query = computed(() => this.queryParamMap().get('q')?.trim() ?? '');
  protected readonly scope = computed<SearchScope>(() => {
    const value = this.queryParamMap().get('scope');

    return value === 'team' || value === 'player' || value === 'coach' || value === 'stadium' || value === 'league' ? value : 'all';
  });

  protected readonly hasQuery = computed(() => this.query().length >= 2);

  protected readonly teams = toSignal(
    this.route.queryParamMap.pipe(
      map((params) => params.get('q')?.trim() ?? ''),
      switchMap((query) =>
        query.length >= 2 ? this.svc.searchTeamsByName(query).pipe(catchError(() => of([] as Team[]))) : of([] as Team[]),
      ),
    ),
    { initialValue: [] as Team[] },
  );

  protected readonly players = toSignal(
    this.route.queryParamMap.pipe(
      map((params) => params.get('q')?.trim() ?? ''),
      switchMap((query) =>
        query.length >= 2 ? this.svc.searchPlayersByName(query).pipe(catchError(() => of([] as Player[]))) : of([] as Player[]),
      ),
    ),
    { initialValue: [] as Player[] },
  );

  protected readonly coaches = toSignal(
    this.route.queryParamMap.pipe(
      map((params) => params.get('q')?.trim() ?? ''),
      switchMap((query) =>
        query.length >= 2 ? this.svc.searchCoachesByName(query).pipe(catchError(() => of([] as Coach[]))) : of([] as Coach[]),
      ),
    ),
    { initialValue: [] as Coach[] },
  );

  protected readonly stadiums = toSignal(this.svc.getStadiums(), { initialValue: [] as Stadium[] });

  protected readonly leagues = toSignal(
    this.route.queryParamMap.pipe(
      map((params) => params.get('q')?.trim() ?? ''),
      switchMap((query) =>
        query.length >= 2 ? this.svc.searchLeaguesByName(query).pipe(catchError(() => of([] as League[]))) : of([] as League[]),
      ),
    ),
    { initialValue: [] as League[] },
  );

  protected readonly results = computed<SearchResult[]>(() => {
    if (!this.hasQuery()) {
      return [];
    }

    return this.searchResultsService.buildResults(
      this.query(),
      this.scope(),
      this.teams(),
      this.players(),
      this.coaches(),
      this.stadiums(),
      this.leagues(),
    );
  });

  protected readonly teamResults = computed(() => this.results().filter((result) => result.kind === 'team'));
  protected readonly playerResults = computed(() => this.results().filter((result) => result.kind === 'player'));
  protected readonly coachResults = computed(() => this.results().filter((result) => result.kind === 'coach'));
  protected readonly stadiumResults = computed(() => this.results().filter((result) => result.kind === 'stadium'));
  protected readonly leagueResults = computed(() => this.results().filter((result) => result.kind === 'league'));
  protected readonly totalResults = computed(() => this.results().length);
}