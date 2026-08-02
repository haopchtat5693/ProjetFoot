import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import type { League, Season, Team } from '../../interfaces/dashboard';

@Component({
  selector: 'app-team-league-lookup-card',
  imports: [CommonModule, FormsModule],
  templateUrl: './team-league-lookup-card.component.html',
  styleUrl: './team-league-lookup-card.component.scss',
})
export class TeamLeagueLookupCardComponent {
  @Input() teamSearchName = '';
  @Input() teamResults: Team[] = [];
  @Input() selectedTeamId: number | null = null;

  @Input() leagueSearchName = '';
  @Input() leagueResults: League[] = [];
  @Input() selectedLeagueId: number | null = null;

  @Input() availableSeasons: Season[] = [];
  @Input() selectedSeasonId: number | null = null;

  @Input() selectedTeamName: string | null = null;
  @Input() selectedLeagueName: string | null = null;
  @Input() selectedCountry: string | null = null;
  @Input() selectedLeagueType: string | null = null;

  @Output() readonly teamSearchNameChange = new EventEmitter<string>();
  @Output() readonly searchTeams = new EventEmitter<void>();
  @Output() readonly teamSelected = new EventEmitter<number>();

  @Output() readonly leagueSearchNameChange = new EventEmitter<string>();
  @Output() readonly searchLeagues = new EventEmitter<void>();
  @Output() readonly leagueSelected = new EventEmitter<number>();

  @Output() readonly seasonSelected = new EventEmitter<number | null>();
}
