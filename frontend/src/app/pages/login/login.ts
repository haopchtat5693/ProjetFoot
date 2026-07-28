import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { switchMap } from 'rxjs';

import { ROLE_OPTIONS } from '../../constants/roles';
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
  protected isRegisterMode = false;

  protected form = {
    username: '',
    password: '',
  };

  protected get submitLabel(): string {
    return this.isRegisterMode ? 'Create account' : 'Login';
  }

  protected get pageTitle(): string {
    return this.isRegisterMode ? 'Create your account' : 'Log in to continue';
  }

  protected get introText(): string {
    return this.isRegisterMode
      ? 'Create a new account, then use it to access the dashboard.'
      : 'Enter your username and password to continue.';
  }

  protected toggleMode(): void {
    this.isRegisterMode = !this.isRegisterMode;
  }

  protected submit(): void {
    const username = this.form.username.trim();
    const password = this.form.password.trim();
    const request$ = this.isRegisterMode
      ? this.auth.register(username, password).pipe(
          switchMap(() => this.auth.login(username, password))
        )
      : this.auth.login(username, password);

    request$.subscribe({
      next: () => {
        void this.router.navigateByUrl('/');
      },
      error: (err) => {
        console.error('Erreur lors de l’authentification', err);
      },
    });
  }
}
