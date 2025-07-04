import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AnalysisResultService {
  private resultSource = new BehaviorSubject<any>(null);

  result$ = this.resultSource.asObservable();

  setResult(result: any) {
    this.resultSource.next(result);
  }

  clearResult() {
    this.resultSource.next(null);
  }
}
