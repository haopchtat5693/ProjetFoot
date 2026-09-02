import { Injectable } from '@angular/core';

import {
  COACH_DEFAULT_SUBTITLE,
  COACH_ROUTE_PREFIX,
  LEAGUE_DEFAULT_SUBTITLE,
  LEAGUE_ROUTE_PREFIX,
  PLAYER_DEFAULT_SUBTITLE,
  PLAYER_ROUTE_PREFIX,
  RESULTS_SEPARATOR,
  SEARCH_RESULT_KIND_COACH,
  SEARCH_RESULT_KIND_LEAGUE,
  SEARCH_RESULT_KIND_PLAYER,
  SEARCH_RESULT_KIND_STADIUM,
  SEARCH_RESULT_KIND_TEAM,
  SEARCH_RESULT_SCOPE_ALL,
  SEATS_SUFFIX,
  STADIUM_ROUTE_PREFIX,
  TEAM_DEFAULT_SUBTITLE,
  TEAM_ROUTE_PREFIX,
} from '../constants/search-results';
import type { League, Player, Stadium, Team, Coach } from '../interfaces/tables';
import type { SearchResult, SearchResultKind, SearchScope } from '../interfaces/search-results';

@Injectable({ providedIn: 'root' })
export class SearchResultsService {
  private readonly maxResults = 100;

  buildResults(
    term: string,
    scope: SearchScope,
    teams: Team[],
    players: Player[],
    coaches: Coach[],
    stadiums: Stadium[],
    leagues: League[],
  ): SearchResult[] {
    const normalizedTerm = term.toLowerCase();
    const results: SearchResult[] = [];

    if (this.allows(scope, SEARCH_RESULT_KIND_TEAM)) {
      results.push(...this.buildTeamResults(normalizedTerm, teams));
    }

    if (this.allows(scope, SEARCH_RESULT_KIND_PLAYER)) {
      results.push(...this.buildPlayerResults(normalizedTerm, players));
    }

    if (this.allows(scope, SEARCH_RESULT_KIND_COACH)) {
      results.push(...this.buildCoachResults(normalizedTerm, coaches));
    }

    if (this.allows(scope, SEARCH_RESULT_KIND_STADIUM)) {
      results.push(...this.buildStadiumResults(normalizedTerm, stadiums));
    }

    if (this.allows(scope, SEARCH_RESULT_KIND_LEAGUE)) {
      results.push(...this.buildLeagueResults(normalizedTerm, leagues));
    }

    return results;
  }

  private allows(scope: SearchScope, kind: SearchResultKind): boolean {
    return scope === SEARCH_RESULT_SCOPE_ALL || scope === kind;
  }

  private matches(term: string, ...values: (string | number | null | undefined)[]): boolean {
    return values.some((value) => String(value ?? '').toLowerCase().includes(term));
  }

  private buildTeamResults(term: string, teams: Team[]): SearchResult[] {
    return teams
      .filter((team) => this.matches(term, team.name, team.country, team.city, team.id))
      .slice(0, this.maxResults)
      .map((team) => ({
        kind: 'team',
        id: team.id,
        title: team.name,
        subtitle: [team.country, team.city].filter(Boolean).join(RESULTS_SEPARATOR) || TEAM_DEFAULT_SUBTITLE,
        route: `${TEAM_ROUTE_PREFIX}${team.id}`,
      }));
  }

  private buildPlayerResults(term: string, players: Player[]): SearchResult[] {
    return players
      .filter((player) => this.matches(term, player.name, player.nationality, player.position, player.id))
      .slice(0, this.maxResults)
      .map((player) => ({
        kind: 'player',
        id: player.id,
        title: player.name,
        subtitle: [player.position, player.nationality].filter(Boolean).join(RESULTS_SEPARATOR) || PLAYER_DEFAULT_SUBTITLE,
        route: `${PLAYER_ROUTE_PREFIX}${player.id}`,
      }));
  }

  private buildCoachResults(term: string, coaches: Coach[]): SearchResult[] {
    return coaches
      .filter((coach) => this.matches(term, coach.name, coach.nationality, coach.id))
      .slice(0, this.maxResults)
      .map((coach) => ({
        kind: 'coach',
        id: coach.id,
        title: coach.name,
        subtitle: coach.nationality || COACH_DEFAULT_SUBTITLE,
        route: `${COACH_ROUTE_PREFIX}${coach.id}`,
      }));
  }

  private buildStadiumResults(term: string, stadiums: Stadium[]): SearchResult[] {
    return stadiums
      .filter((stadium) => this.matches(term, stadium.name, stadium.city, stadium.address, stadium.id))
      .slice(0, this.maxResults)
      .map((stadium) => ({
        kind: 'stadium',
        id: stadium.id,
        title: stadium.name,
        subtitle: [stadium.city, `${stadium.capacity} ${SEATS_SUFFIX}`].filter(Boolean).join(RESULTS_SEPARATOR),
        route: `${STADIUM_ROUTE_PREFIX}${stadium.id}`,
      }));
  }

  private buildLeagueResults(term: string, leagues: League[]): SearchResult[] {
    return leagues
      .filter((league) => this.matches(term, league.name, league.country, league.league_type, league.id))
      .slice(0, this.maxResults)
      .map((league) => ({
        kind: 'league',
        id: league.id,
        title: league.name,
        subtitle: [league.country, league.league_type].filter(Boolean).join(RESULTS_SEPARATOR) || LEAGUE_DEFAULT_SUBTITLE,
        route: `${LEAGUE_ROUTE_PREFIX}${league.id}`,
      }));
  }
}
