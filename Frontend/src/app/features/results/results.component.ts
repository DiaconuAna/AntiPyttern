import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import {AnalysisResultService} from "../../services/analysis-result.service";
import { BlobResultsComponent } from './blob-results/blob-results.component';
import { SpaghettiResultsComponent } from './spaghetti-results/spaghetti-results.component';
import {SakResultsComponent} from "./sak-results/sak-results.component";

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule, BlobResultsComponent, SpaghettiResultsComponent, SakResultsComponent],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css'
})
export class ResultsComponent {
  resultsResponse: any = null;
  objectKeys = Object.keys;
  expandedFiles = new Set<string>();

  constructor(private analysisResultService: AnalysisResultService) {
    this.analysisResultService.result$.subscribe(result => {
      this.resultsResponse = result;
    });
  }
}
