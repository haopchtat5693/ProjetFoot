import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { ApiService } from '../../services/api.service';
import type { Team } from '../../interfaces/tables';

@Component({
  selector: 'app-teams',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './teams.html',
  styleUrl: './teams.scss',
})
export class Teams {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected teams = toSignal(this.svc.getTeams(), { initialValue: [] as Team[] });
  protected searchQuery = signal('');
  protected countryFilter = signal('all');
  protected readonly queryParamMap = toSignal(this.route.queryParamMap, {
    initialValue: this.route.snapshot.queryParamMap,
  });

  constructor() {
    this.searchQuery.set(this.queryParamMap().get('search') ?? '');
    this.countryFilter.set(this.queryParamMap().get('country') ?? 'all');
  }

  protected countryOptions = computed(() => {
    const countries = this.teams()
      .map((team) => team.country?.trim())
      .filter((country): country is string => !!country);

    return ['all', ...Array.from(new Set(countries)).sort((a, b) => a.localeCompare(b))];
  });

  protected filteredTeams = computed(() => {
    const searchTerm = this.searchQuery().trim().toLowerCase();
    const country = this.countryFilter();

    return this.teams()
      .filter((team) => {
        const matchesSearch =
          !searchTerm ||
          [team.name, team.city, team.country, String(team.id)].some(
            (value) => value?.toLowerCase().includes(searchTerm),
          );

        const matchesCountry = country === 'all' || team.country === country;

        return matchesSearch && matchesCountry;
      })
      .sort((left, right) => left.name.localeCompare(right.name));
  });
}
