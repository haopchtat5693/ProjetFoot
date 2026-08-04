import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type {
  League,
  LeagueLookupQuery,
  Stadium,
  Team,
  Season,
  Player,
  PlayerSeasonStats,
  TeamSeasonStats,
} from '../interfaces/dashboard';

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://127.0.0.1:8000';

  getTeams(): Observable<Team[]> {
    return this.http.get<Team[]>(`${this.apiUrl}/teams`);
  }

  getTeamById(teamId: number): Observable<Team> {
    return this.http.get<Team>(`${this.apiUrl}/teams/${teamId}`);
  }

  searchTeamsByName(name: string): Observable<Team[]> {
    const params = new URLSearchParams({ name });

    return this.http.get<Team[]>(`${this.apiUrl}/teams/search?${params.toString()}`);
  }

  getSeasons(): Observable<Season[]> {
    return this.http.get<Season[]>(`${this.apiUrl}/seasons`);
  }

  getStadiums(): Observable<Stadium[]> {
    return this.http.get<Stadium[]>(`${this.apiUrl}/stadiums`);
  }

  getStadiumById(stadiumId: number): Observable<Stadium> {
    return this.http.get<Stadium>(`${this.apiUrl}/stadiums/${stadiumId}`);
  }

  getLeagues(): Observable<League[]> {
    return this.http.get<League[]>(`${this.apiUrl}/leagues`);
  }

  getLeagueById(leagueId: number): Observable<League> {
    return this.http.get<League>(`${this.apiUrl}/leagues/${leagueId}`);
  }

  lookupLeagues(query: LeagueLookupQuery): Observable<League[]> {
    const params = new URLSearchParams();

    Object.entries(query).forEach(([key, value]) => {
      if (value === null || value === undefined || value === '') {
        return;
      }

      params.set(key, String(value));
    });

    if (params.has('id')) {
      params.set('id', params.get('id') ?? '');
    }

    if (params.has('type')) {
      params.set('type', params.get('type') ?? '');
    }

    const queryString = params.toString();
    const suffix = queryString ? `?${queryString}` : '';

    return this.http.get<League[]>(`${this.apiUrl}/leagues/lookup${suffix}`);
  }

  getTeamPlayersForSeason(teamId: number, seasonId: number): Observable<Player[]> {
    return this.http.get<Player[]>(`${this.apiUrl}/teams/${teamId}/seasons/${seasonId}/players`);
  }

  getTeamSeasonStats(teamId: number, leagueId: number, seasonId: number): Observable<TeamSeasonStats> {
    return this.http.get<TeamSeasonStats>(
      `${this.apiUrl}/stats/team/${teamId}/league/${leagueId}/season/${seasonId}`,
    );
  }

  getPlayers(): Observable<Player[]> {
    return this.http.get<Player[]>(`${this.apiUrl}/players`);
  }

  getPlayerById(playerId: number): Observable<Player> {
    return this.http.get<Player>(`${this.apiUrl}/players/${playerId}`);
  }

  searchPlayersByName(
    name: string,
  ): Observable<Player[]> {
    const params = new URLSearchParams({ name });

    return this.http.get<Player[]>(`${this.apiUrl}/players/search?${params.toString()}`);
  }

  getPlayerSeasonStats(playerId: number, seasonId: number): Observable<PlayerSeasonStats> {
    return this.http.get<PlayerSeasonStats>(`${this.apiUrl}/stats/player/${playerId}/season/${seasonId}`);
  }
}
