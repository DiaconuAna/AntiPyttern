import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-blob-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './blob-results.component.html',
  styleUrl: './blob-results.component.css'
})
export class BlobResultsComponent {
  @Input() blobResults: any[] = [];
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
