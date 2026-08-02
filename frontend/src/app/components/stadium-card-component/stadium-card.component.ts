import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import type { Stadium } from '../../interfaces/dashboard';

@Component({
  selector: 'app-stadium-card',
  imports: [CommonModule],
  templateUrl: './stadium-card.component.html',
  styleUrls: ['./stadium-card.component.scss'],
})
export class StadiumCardComponent {
  @Input({ required: true }) stadium!: Stadium;
}
