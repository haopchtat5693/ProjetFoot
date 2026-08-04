import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

type SearchScope = 'all' | 'team' | 'player' | 'stadium' | 'league';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app-shell.html',
  styleUrl: './app.scss'
})
export class App {
  private readonly router = inject(Router);

  protected readonly title = signal('frontend');
  protected searchScope = signal<SearchScope>('all');
  protected query = signal('');

  protected onSearchInput(value: string): void {
    this.query.set(value);
  }

  protected onScopeChange(value: string): void {
    const nextScope: SearchScope = value === 'team' || value === 'player' || value === 'stadium' || value === 'league' ? value : 'all';

    this.searchScope.set(nextScope);
  }

  protected submitSearch(): void {
    const term = this.query().trim();

    if (term.length < 2) {
      return;
    }

    void this.router.navigate(['/search'], {
      queryParams: {
        q: term,
        scope: this.searchScope(),
      },
    });
  }

  protected onSearchSubmit(event: Event): void {
    event.preventDefault();
    this.submitSearch();
  }
}
