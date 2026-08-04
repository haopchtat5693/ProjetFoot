import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, map, of, startWith, switchMap } from 'rxjs';
import { DashboardService } from '../../services/dashboard.service';
import type { Stadium } from '../../interfaces/dashboard';

@Component({
  selector: 'app-stadium-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './stadium-detail.html',
  styleUrl: './stadium-detail.scss',
})
export class StadiumDetail {
  private readonly svc = inject(DashboardService);
  private readonly route = inject(ActivatedRoute);

  protected readonly stadium = toSignal<Stadium | null>(
    this.route.paramMap.pipe(
      map((params) => params.get('stadiumId')),
      switchMap((rawStadiumId) => {
        const stadiumId = Number(rawStadiumId);
        return rawStadiumId && Number.isFinite(stadiumId)
          ? this.svc.getStadiumById(stadiumId)
          : of(null as Stadium | null);
      }),
      startWith(null as Stadium | null),
      catchError(() => of(null as Stadium | null)),
    ),
    { requireSync: true },
  );

  protected readonly highlights = computed(() => {
    const stadium = this.stadium();
    if (!stadium) return [] as { label: string; value: string }[];

    return [
      { label: 'ID', value: String(stadium.id) },
      { label: 'City', value: stadium.city || 'Unknown' },
      { label: 'Capacity', value: String(stadium.capacity) },
      { label: 'Address', value: stadium.address || 'Unknown' },
    ];
  });
}