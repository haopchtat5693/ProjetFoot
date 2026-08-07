import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { switchMap } from 'rxjs';

import {
  AUTH_ERROR_MESSAGE,
  CREATE_ACCOUNT_INTRO_TEXT,
  CREATE_ACCOUNT_LABEL,
  CREATE_ACCOUNT_TITLE,
  LOGIN_INTRO_TEXT,
  LOGIN_LABEL,
  LOGIN_TITLE,
  SEARCH_ROUTE,
} from '../../constants/login';
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
    return this.isRegisterMode ? CREATE_ACCOUNT_LABEL : LOGIN_LABEL;
  }

  protected get pageTitle(): string {
    return this.isRegisterMode ? CREATE_ACCOUNT_TITLE : LOGIN_TITLE;
  }

  protected get introText(): string {
    return this.isRegisterMode ? CREATE_ACCOUNT_INTRO_TEXT : LOGIN_INTRO_TEXT;
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
        void this.router.navigateByUrl(SEARCH_ROUTE);
      },
      error: (err) => {
        console.error(AUTH_ERROR_MESSAGE, err);
      },
    });
  }
}
