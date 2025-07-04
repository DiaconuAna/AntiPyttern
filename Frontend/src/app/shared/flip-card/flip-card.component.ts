import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-flip-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './flip-card.component.html',
  styleUrls: ['./flip-card.component.css']
})
export class FlipCardComponent {
  @Input() height = 'h-64';
  @Input() flipped = false;

  toggleFlip() {
    this.flipped = !this.flipped;
  }
}
