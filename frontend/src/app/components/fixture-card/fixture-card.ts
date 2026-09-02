import { Component, Input, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import type { Fixture, Team } from '../../interfaces/tables';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-fixture-card',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './fixture-card.html',
  styleUrl: './fixture-card.scss',
})
export class FixtureCardComponent implements OnInit {
  @Input() fixture!: Fixture;

  private readonly api = inject(ApiService);

  protected readonly homeTeam = signal<Team | null>(null);
  protected readonly awayTeam = signal<Team | null>(null);
  protected readonly loading = signal(true);

  ngOnInit(): void {
    if (!this.fixture) return;

    // Fetch home team
    this.api
      .getTeamById(this.fixture.home_team_id)
      .pipe(catchError(() => of(null)))
      .subscribe((team) => {
        this.homeTeam.set(team);
        this.checkLoadingComplete();
      });

    // Fetch away team
    this.api
      .getTeamById(this.fixture.away_team_id)
      .pipe(catchError(() => of(null)))
      .subscribe((team) => {
        this.awayTeam.set(team);
        this.checkLoadingComplete();
      });
  }

  private checkLoadingComplete(): void {
    if (this.homeTeam() && this.awayTeam()) {
      this.loading.set(false);
    }
  }

  protected getTeamName(team: Team | null, teamId: number): string {
    return team?.name ?? `Team #${teamId}`;
  }

  protected getTeamLogo(team: Team | null): string | null {
    return team?.logo ?? null;
  }

  protected getDateDisplay(): string {
    if (!this.fixture.date) return '—';
    const date = new Date(this.fixture.date);
    return `${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`;
  }

  protected getTimeDisplay(): string {
    if (!this.fixture.date) return '';
    const date = new Date(this.fixture.date);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  }

  protected getScoreDisplay(): string {
    const home = this.fixture.home_goals ?? '—';
    const away = this.fixture.away_goals ?? '—';
    return `${home} - ${away}`;
  }

  protected getStatusClass(): string {
    const status = this.fixture.status?.toLowerCase() ?? '';
    if (status === 'ft' || status === 'aet') return 'finished';
    if (status === 'live' || status === '1h' || status === '2h') return 'live';
    if (status === 'pstz' || status === 'pend') return 'pending';
    return 'pending';
  }

  protected getStatusText(): string {
    const status = this.fixture.status?.toUpperCase() ?? '—';
    if (status === 'FT') return 'Full Time';
    if (status === 'AET') return 'After Extra Time';
    if (status === '1H') return '1st Half';
    if (status === '2H') return '2nd Half';
    if (status === 'LIVE') return 'Live';
    if (status === 'PSTZ') return 'Postponed';
    if (status === 'PEND') return 'Pending';
    return status;
  }

  protected onFixtureClick(): void {
    console.log('[FixtureCard] Clicked fixture:', {
      id: this.fixture.id,
      home_team_id: this.fixture.home_team_id,
      away_team_id: this.fixture.away_team_id,
      league_id: this.fixture.league_id,
      season_id: this.fixture.season_id,
      home_team_name: this.homeTeam()?.name,
      away_team_name: this.awayTeam()?.name,
      home_goals: this.fixture.home_goals,
      away_goals: this.fixture.away_goals,
    });
  }
}
