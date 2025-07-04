import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-spaghetti-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './spaghetti-results.component.html'
})
export class SpaghettiResultsComponent {
  @Input() spaghettiResults: any[] = [];
  objectKeys = Object.keys;
  expandedFiles = new Set<string>();

  toggleFile(fileName: string) {
    if (this.expandedFiles.has(fileName)) {
      this.expandedFiles.delete(fileName);
    } else {
      this.expandedFiles.add(fileName);
    }
  }

  isExpanded(fileName: string): boolean {
    return this.expandedFiles.has(fileName);
  }
}
