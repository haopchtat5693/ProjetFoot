import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { DEFAULT_ROLE, ROLE_OPTIONS } from '../../constants/roles';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly roles = ROLE_OPTIONS;

  protected form = {
    name: '',
    password: '',
    email: '',
  };

  protected submit(): void {
    this.auth.login(
      this.form.name.trim(),
      this.form.password.trim(),
      this.form.email.trim()
    ).subscribe({
      next: () => {
        void this.router.navigateByUrl('/');
      },
    });
  }
}
