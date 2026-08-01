import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { Team, Season, Player, PlayerSeasonStats } from '../interfaces/dashboard';

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://127.0.0.1:8000';

  getTeams(): Observable<Team[]> {
    return this.http.get<Team[]>(`${this.apiUrl}/teams`);
  }

  searchTeamsByName(name: string): Observable<Team[]> {
    const params = new URLSearchParams({ name });

    return this.http.get<Team[]>(`${this.apiUrl}/teams/search?${params.toString()}`);
  }

  getSeasons(): Observable<Season[]> {
    return this.http.get<Season[]>(`${this.apiUrl}/seasons`);
  }

  getTeamPlayersForSeason(teamId: number, seasonId: number): Observable<Player[]> {
    return this.http.get<Player[]>(`${this.apiUrl}/teams/${teamId}/seasons/${seasonId}/players`);
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
