import {Component, Input} from '@angular/core';
import {NgClass, TitleCasePipe} from "@angular/common";
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-sak-results',
  standalone: true,
  imports: [
    TitleCasePipe,
    NgClass,
    CommonModule,
  ],
  templateUrl: './sak-results.component.html',
  styleUrl: './sak-results.component.css'
})
export class SakResultsComponent {
  @Input() sakResults: any[] = [];
  objectKeys = Object.keys;

  expandedFiles = new Set<string>();

  toggleFile(filePath: string): void {
    if (this.expandedFiles.has(filePath)) {
      this.expandedFiles.delete(filePath);
    } else {
      this.expandedFiles.add(filePath);
    }
  }

  isExpanded(filePath: string): boolean {
    return this.expandedFiles.has(filePath);
  }

}
