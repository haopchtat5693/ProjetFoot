import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { toSignal } from '@angular/core/rxjs-interop';
import { DashboardService } from '../../services/dashboard.service';
import type { Stadium } from '../../interfaces/dashboard';
import { StadiumCardComponent } from '../../components/stadium-card-component/stadium-card.component';

@Component({
  selector: 'app-stadiums',
  imports: [CommonModule, FormsModule, StadiumCardComponent],
  templateUrl: './stadiums.html',
  styleUrl: './stadiums.scss',
})
export class Stadiums {
  private readonly svc = inject(DashboardService);

  protected stadiums = toSignal(this.svc.getStadiums(), { initialValue: [] as Stadium[] });
  protected searchQuery = signal('');
  protected cityFilter = signal('all');

  protected cityOptions = computed(() => {
    const cities = this.stadiums()
      .map((stadium) => stadium.city?.trim())
      .filter((city): city is string => !!city);

    return ['all', ...Array.from(new Set(cities)).sort((a, b) => a.localeCompare(b))];
  });

  protected filteredStadiums = computed(() => {
    const searchTerm = this.searchQuery().trim().toLowerCase();
    const city = this.cityFilter();

    return this.stadiums()
      .filter((stadium) => {
        const matchesSearch =
          !searchTerm ||
          [stadium.name, stadium.city, stadium.address, String(stadium.capacity), String(stadium.id)].some(
            (value) => value?.toLowerCase().includes(searchTerm),
          );

        const matchesCity = city === 'all' || stadium.city === city;

        return matchesSearch && matchesCity;
      })
      .sort((left, right) => left.name.localeCompare(right.name));
  });
}
