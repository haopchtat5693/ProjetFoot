import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import type { Player, Season } from '../../interfaces/dashboard';

@Component({
  selector: 'app-player-lookup-card',
  imports: [CommonModule, FormsModule],
  templateUrl: './player-lookup-card.component.html',
  styleUrls: ['./player-lookup-card.component.scss'],
})
export class PlayerLookupCardComponent {
  @Input() playerSearchName = '';
  @Input() playerResults: Player[] = [];
  @Input() selectedPlayerId: number | null = null;

  @Input() playerSeasons: Season[] = [];
  @Input() selectedPlayerSeasonId: number | null = null;

  @Output() readonly playerSearchNameChange = new EventEmitter<string>();
  @Output() readonly searchPlayers = new EventEmitter<void>();
  @Output() readonly playerSelected = new EventEmitter<number | null>();
  @Output() readonly playerSeasonSelected = new EventEmitter<number | null>();
  @Output() readonly fetchPlayerStats = new EventEmitter<void>();
}
