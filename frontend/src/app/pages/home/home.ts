import { Component, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-home',
  imports: [RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly isConnected = this.auth.isAuthenticated;

  protected logout(): void {
    this.auth.logout().subscribe({
      next: () => {
        void this.router.navigateByUrl('/');
      },
    });
  }
}
  