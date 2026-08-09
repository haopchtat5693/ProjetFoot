import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import type { DetailHighlight } from '../../interfaces/detail';
import { createDetailHighlight, createRouteEntitySignal } from '../../utils';

@Component({
  selector: 'app-coach-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './coach-detail.html',
  styleUrl: './coach-detail.scss',
})
export class CoachDetail {
  private readonly svc = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected readonly coach = createRouteEntitySignal(this.route, 'coachId', (coachId) =>
    this.svc.getCoachById(coachId),
  );

  protected readonly highlights = computed<DetailHighlight[]>(() => {
    const coach = this.coach();
    if (!coach) return [];

    return [
      createDetailHighlight('ID', coach.id),
      createDetailHighlight('Nationality', coach.nationality),
      createDetailHighlight('Age', coach.age),
    ];
  });

  protected readonly careerHistory = computed(() => {
    const coach = this.coach();
    if (!coach || !coach.career) return [];

    return coach.career;
  });
}
