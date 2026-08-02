import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { toSignal } from '@angular/core/rxjs-interop';
import { DashboardService } from '../../services/dashboard.service';
import type { Player } from '../../interfaces/dashboard';

@Component({
  selector: 'app-players',
  imports: [CommonModule, FormsModule],
  templateUrl: './players.html',
  styleUrl: './players.scss',
})
export class Players {
  private readonly svc = inject(DashboardService);

  protected players = toSignal(this.svc.getPlayers(), { initialValue: [] as Player[] });
  protected searchQuery = signal('');
  protected positionFilter = signal('all');
  protected countryFilter = signal('all');

  protected positionOptions = computed(() => {
    const positions = this.players()
      .map((player) => player.position?.trim())
      .filter((position): position is string => !!position);

    return ['all', ...Array.from(new Set(positions)).sort((a, b) => a.localeCompare(b))];
  });

  protected countryOptions = computed(() => {
    const countries = this.players()
      .map((player) => player.country?.trim())
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
          [player.name, player.position, player.country, String(player.id)].some((value) =>
            value?.toLowerCase().includes(searchTerm),
          );

        const matchesPosition = position === 'all' || player.position === position;
        const matchesCountry = country === 'all' || player.country === country;

        return matchesSearch && matchesPosition && matchesCountry;
      })
      .sort((left, right) => left.name.localeCompare(right.name));
  });
}
