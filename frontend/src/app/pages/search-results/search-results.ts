import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, map, of, switchMap } from 'rxjs';
import { DashboardService } from '../../services/dashboard.service';
import type { League, Player, Stadium, Team } from '../../interfaces/dashboard';

type SearchResultKind = 'team' | 'player' | 'stadium' | 'league';
type SearchScope = 'all' | SearchResultKind;

interface SearchResult {
  kind: SearchResultKind;
  id: number;
  title: string;
  subtitle: string;
  route: string;
}

@Component({
  selector: 'app-search-results',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './search-results.html',
  styleUrl: './search-results.scss',
})
export class SearchResults {
  private readonly svc = inject(DashboardService);
  private readonly route = inject(ActivatedRoute);

  protected readonly queryParamMap = toSignal(this.route.queryParamMap, {
    initialValue: this.route.snapshot.queryParamMap,
  });

  protected readonly query = computed(() => this.queryParamMap().get('q')?.trim() ?? '');
  protected readonly scope = computed<SearchScope>(() => {
    const value = this.queryParamMap().get('scope');

    return value === 'team' || value === 'player' || value === 'stadium' || value === 'league' ? value : 'all';
  });

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
  protected readonly stadiums = toSignal(this.svc.getStadiums(), { initialValue: [] as Stadium[] });
  protected readonly leagues = toSignal(this.svc.getLeagues(), { initialValue: [] as League[] });

  protected readonly teamResults = computed(() => this.buildTeamResults());
  protected readonly playerResults = computed(() => this.buildPlayerResults());
  protected readonly stadiumResults = computed(() => this.buildStadiumResults());
  protected readonly leagueResults = computed(() => this.buildLeagueResults());
  protected readonly totalResults = computed(
    () => this.teamResults().length + this.playerResults().length + this.stadiumResults().length + this.leagueResults().length,
  );

  protected get hasQuery(): boolean {
    return this.query().length >= 2;
  }

  private matches(term: string, ...values: (string | number | null | undefined)[]): boolean {
    return values.some((value) => String(value ?? '').toLowerCase().includes(term));
  }

  private allows(kind: SearchResultKind): boolean {
    const scope = this.scope();
    return scope === 'all' || scope === kind;
  }

  private buildTeamResults(): SearchResult[] {
    const term = this.query().toLowerCase();

    if (!this.hasQuery || !this.allows('team')) return [];

    return this.teams()
      .filter((team) => this.matches(term, team.name, team.country, team.city, team.id))
      .slice(0, 100)
      .map((team) => ({
        kind: 'team' as const,
        id: team.id,
        title: team.name,
        subtitle: [team.country, team.city].filter(Boolean).join(' · ') || 'Team',
        route: `/teams/${team.id}`,
      }));
  }

  private buildPlayerResults(): SearchResult[] {
    const term = this.query().toLowerCase();

    if (!this.hasQuery || !this.allows('player')) return [];

    return this.players()
      .filter((player) => this.matches(term, player.name, player.nationality, player.position, player.id))
      .slice(0, 100)
      .map((player) => ({
        kind: 'player' as const,
        id: player.id,
        title: player.name,
        subtitle: [player.position, player.nationality].filter(Boolean).join(' · ') || 'Player',
        route: `/players/${player.id}`,
      }));
  }

  private buildStadiumResults(): SearchResult[] {
    const term = this.query().toLowerCase();

    if (!this.hasQuery || !this.allows('stadium')) return [];

    return this.stadiums()
      .filter((stadium) => this.matches(term, stadium.name, stadium.city, stadium.address, stadium.id))
      .slice(0, 100)
      .map((stadium) => ({
        kind: 'stadium' as const,
        id: stadium.id,
        title: stadium.name,
        subtitle: [stadium.city, `${stadium.capacity} seats`].filter(Boolean).join(' · '),
        route: `/stadiums/${stadium.id}`,
      }));
  }

  private buildLeagueResults(): SearchResult[] {
    const term = this.query().toLowerCase();

    if (!this.hasQuery || !this.allows('league')) return [];

    return this.leagues()
      .filter((league) => this.matches(term, league.name, league.country, league.league_type, league.id))
      .slice(0, 100)
      .map((league) => ({
        kind: 'league' as const,
        id: league.id,
        title: league.name,
        subtitle: [league.country, league.league_type].filter(Boolean).join(' · ') || 'League',
        route: `/leagues/${league.id}`,
      }));
  }
}