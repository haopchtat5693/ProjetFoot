import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { ApiService } from '../../services/api.service';
import type { League } from '../../interfaces/dashboard';

@Component({
  selector: 'app-leagues',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './leagues.html',
  styleUrl: './leagues.scss',
})
export class Leagues {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected leagues = toSignal(this.svc.getLeagues(), { initialValue: [] as League[] });
  protected searchQuery = signal('');
  protected countryFilter = signal('all');
  protected typeFilter = signal('all');
  protected readonly queryParamMap = toSignal(this.route.queryParamMap, {
    initialValue: this.route.snapshot.queryParamMap,
  });

  protected countryOptions = computed(() => {
    const countries = this.leagues()
      .map((league) => league.country?.trim())
      .filter((country): country is string => !!country);

    return ['all', ...Array.from(new Set(countries)).sort((a, b) => a.localeCompare(b))];
  });

  protected typeOptions = computed(() => {
    const types = this.leagues()
      .map((league) => league.league_type?.trim())
      .filter((type): type is string => !!type);

    return ['all', ...Array.from(new Set(types)).sort((a, b) => a.localeCompare(b))];
  });

  protected filteredLeagues = computed(() => {
    const searchTerm = this.searchQuery().trim().toLowerCase();
    const country = this.countryFilter();
    const type = this.typeFilter();

    return this.leagues()
      .filter((league) => {
        const matchesSearch =
          !searchTerm ||
          [league.name, league.country, league.league_type, String(league.id)].some((value) =>
            value?.toLowerCase().includes(searchTerm),
          );

        const matchesCountry = country === 'all' || league.country === country;
        const matchesType = type === 'all' || league.league_type === type;

        return matchesSearch && matchesCountry && matchesType;
      })
      .sort((left, right) => left.name.localeCompare(right.name));
  });

  protected seasonCount(league: League): number {
    return league.seasons?.length ?? 0;
  }

  constructor() {
    this.searchQuery.set(this.queryParamMap().get('search') ?? '');
    this.countryFilter.set(this.queryParamMap().get('country') ?? 'all');
    this.typeFilter.set(this.queryParamMap().get('type') ?? 'all');
  }
}