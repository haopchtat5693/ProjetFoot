import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { ApiService } from '../../services/api.service';
import type { Player } from '../../interfaces/tables';

@Component({
  selector: 'app-players',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './players.html',
  styleUrl: './players.scss',
})
export class Players {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected players = toSignal(this.svc.getPlayers(), { initialValue: [] as Player[] });
  protected searchQuery = signal('');
  protected positionFilter = signal('all');
  protected countryFilter = signal('all');
  protected readonly queryParamMap = toSignal(this.route.queryParamMap, {
    initialValue: this.route.snapshot.queryParamMap,
  });

  constructor() {
    this.searchQuery.set(this.queryParamMap().get('search') ?? '');
    this.positionFilter.set(this.queryParamMap().get('position') ?? 'all');
    this.countryFilter.set(this.queryParamMap().get('country') ?? 'all');
  }

  protected positionOptions = computed(() => {
    const positions = this.players()
      .map((player) => player.position?.trim())
      .filter((position): position is string => !!position);

    return ['all', ...Array.from(new Set(positions)).sort((a, b) => a.localeCompare(b))];
  });

  protected countryOptions = computed(() => {
    const countries = this.players()
      .map((player) => player.nationality?.trim())
      .filter((country): country is string => !!country);

    return ['all', ...Array.from(new Set(countries)).sort((a, b) => a.localeCompare(b))];
  });

  protected filteredPlayers = computed(() => {
    const searchTerm = this.searchQuery().trim().toLowerCase();
    const position = this.positionFilter();
    const country = this.countryFilter();

    return this.players()
      .filter((player) => {
        const matchesSearch =
          !searchTerm ||
          [player.name, player.position, player.nationality, String(player.id)].some((value) =>
            value?.toLowerCase().includes(searchTerm),
          );

        const matchesPosition = position === 'all' || player.position === position;
        const matchesCountry = country === 'all' || player.nationality === country;

        return matchesSearch && matchesPosition && matchesCountry;
      })
      .sort((left, right) => left.name.localeCompare(right.name));
  });
}
