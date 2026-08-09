import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { ApiService } from '../../services/api.service';
import type { Coach } from '../../interfaces/dashboard';

@Component({
  selector: 'app-coaches',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './coaches.html',
  styleUrl: './coaches.scss',
})
export class Coaches {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected coaches = toSignal(this.svc.getCoaches(), { initialValue: [] as Coach[] });
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
    const countries = this.coaches()
      .map((coach) => coach.nationality?.trim())
      .filter((country): country is string => !!country);

    return ['all', ...Array.from(new Set(countries)).sort((a, b) => a.localeCompare(b))];
  });

  protected filteredCoaches = computed(() => {
    const searchTerm = this.searchQuery().trim().toLowerCase();
    const country = this.countryFilter();

    return this.coaches()
      .filter((coach) => {
        const matchesSearch =
          !searchTerm ||
          [coach.name, coach.nationality, String(coach.id)].some(
            (value) => value?.toLowerCase().includes(searchTerm),
          );

        const matchesCountry = country === 'all' || coach.nationality === country;

        return matchesSearch && matchesCountry;
      })
      .sort((left, right) => left.name.localeCompare(right.name));
  });
}
