import { Routes } from '@angular/router';
import { DetectionComponent } from './features/detection/detection.component';
import { SpecificationComponent } from './features/specification/specification.component';
import { ResultsComponent } from './features/results/results.component';


export const routes: Routes = [
  { path: '', redirectTo: 'detection', pathMatch: 'full' },
  { path: 'detection', component: DetectionComponent },
  { path: 'specification', component: SpecificationComponent },
  { path: 'results', component: ResultsComponent },
  { path: '**', redirectTo: 'detection' }
];
