import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import type { DetailHighlight } from '../../interfaces/detail';
import { createDetailHighlight, createRouteEntitySignal } from '../../utils';

@Component({
  selector: 'app-stadium-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './stadium-detail.html',
  styleUrl: './stadium-detail.scss',
})
export class StadiumDetail {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected readonly stadium = createRouteEntitySignal(this.route, 'stadiumId', (stadiumId) =>
    this.svc.getStadiumById(stadiumId),
  );

  protected readonly highlights = computed<DetailHighlight[]>(() => {
    const stadium = this.stadium();
    if (!stadium) return [];

    return [
      createDetailHighlight('ID', stadium.id),
      createDetailHighlight('City', stadium.city),
      createDetailHighlight('Capacity', stadium.capacity),
      createDetailHighlight('Address', stadium.address),
    ];
  });
}