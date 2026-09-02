import { CommonModule } from '@angular/common';
import { Component, computed, effect, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import type { DetailHighlight } from '../../interfaces/detail';
import { catchError, of } from 'rxjs';
import { createDetailHighlight, createRouteEntitySignal } from '../../utils';
import type { Team } from '../../interfaces/tables';

@Component({
  selector: 'app-fixture-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './fixture-detail.html',
  styleUrl: './fixture-detail.scss',
})
export class FixtureDetail {
  private readonly api = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected readonly fixture = createRouteEntitySignal(this.route, 'fixtureId', (fixtureId) =>
    this.api.getFixtureById(fixtureId),
  );

  protected readonly homeTeam = signal<Team | null>(null);
  protected readonly awayTeam = signal<Team | null>(null);

  protected readonly statistics = signal<Record<string, unknown> | null>(null);

  protected readonly highlights = computed<DetailHighlight[]>(() => {
    const fixture = this.fixture();
    if (!fixture) return [];
    return [
      createDetailHighlight('ID', fixture.id),
      createDetailHighlight('Status', fixture.status || 'N/A'),
      createDetailHighlight('Date', fixture.date),
      createDetailHighlight('Location', fixture.location),
      createDetailHighlight('League', fixture.league_id ? `#${fixture.league_id}` : 'N/A'),
      createDetailHighlight('Season', fixture.season_id ? `#${fixture.season_id}` : 'N/A'),
    ];
  });

  protected readonly scoreHighlights = computed<DetailHighlight[]>(() => {
    const fixture = this.fixture();
    if (!fixture) return [];
    return [
      createDetailHighlight('Home Team', fixture.home_team_id),
      createDetailHighlight('Away Team', fixture.away_team_id),
      createDetailHighlight('Home Goals', fixture.home_goals ?? 'N/A'),
      createDetailHighlight('Away Goals', fixture.away_goals ?? 'N/A'),
    ];
  });

  constructor() {
    effect((onCleanup) => {
      const fixtureData = this.fixture();
      console.log('[FixtureDetail] Fixture loaded:', { 
        id: fixtureData?.id, 
        home_team_id: fixtureData?.home_team_id, 
        away_team_id: fixtureData?.away_team_id, 
        league_id: fixtureData?.league_id, 
        season_id: fixtureData?.season_id,
        status: fixtureData?.status
      });
      if (!fixtureData) {
        this.homeTeam.set(null);
        this.awayTeam.set(null);
        return;
      }

      this.api
        .getTeamById(fixtureData.home_team_id)
        .pipe(catchError(() => of(null)))
        .subscribe((team) => {
          this.homeTeam.set(team);
        });

      this.api
        .getTeamById(fixtureData.away_team_id)
        .pipe(catchError(() => of(null)))
        .subscribe((team) => {
          this.awayTeam.set(team);
        });

      const statsSubscription = this.api
        .getFixtureStatistics(fixtureData.id)
        .pipe(catchError(() => of(null)))
        .subscribe((stats) => {
          console.log('[FixtureDetail] Statistics loaded for fixture:', fixtureData.id);
          this.statistics.set(stats);
        });

      onCleanup(() => {
        statsSubscription.unsubscribe();
      });
    });
  }

  protected formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  protected getStatusClass(status: string | null | undefined): string {
    if (!status) return 'status-unknown';
    const lowerStatus = status.toLowerCase();
    if (lowerStatus === 'ft') return 'status-finished';
    if (lowerStatus === 'live' || lowerStatus === 'ht') return 'status-live';
    if (lowerStatus === 'pstsup' || lowerStatus === 'susp') return 'status-suspended';
    return 'status-scheduled';
  }

  protected getInitial(name: unknown): string {
    if (!name) return '?';
    const nameStr = typeof name === 'string' ? name : String(name);
    return nameStr.charAt(0).toUpperCase();
  }
}
