import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { ApiService } from '../../services/api.service';
import type { Fixture } from '../../interfaces/tables';

@Component({
  selector: 'app-fixtures',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './fixtures.html',
  styleUrl: './fixtures.scss',
})
export class Fixtures {
  private readonly api = inject(ApiService);

  protected fixtures = toSignal(this.api.getFixtures(), { initialValue: [] as Fixture[] });
  protected searchQuery = signal('');
  protected statusFilter = signal('all');

  protected statusOptions = computed(() => {
    const statuses = this.fixtures()
      .map((fixture) => fixture.status?.trim())
      .filter((status): status is string => !!status);

    return ['all', ...Array.from(new Set(statuses)).sort((a, b) => a.localeCompare(b))];
  });

  protected filteredFixtures = computed(() => {
    const searchTerm = this.searchQuery().trim().toLowerCase();
    const status = this.statusFilter();

    return this.fixtures()
      .filter((fixture) => {
        const matchesSearch =
          !searchTerm ||
          [
            fixture.location,
            String(fixture.id),
            String(fixture.home_team_id),
            String(fixture.away_team_id),
          ].some((value) => value?.toLowerCase().includes(searchTerm));

        const matchesStatus = status === 'all' || fixture.status === status;

        return matchesSearch && matchesStatus;
      })
      .sort((left, right) => {
        // Sort by date descending (newest first)
        return new Date(right.date).getTime() - new Date(left.date).getTime();
      });
  });

  protected formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
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
}
