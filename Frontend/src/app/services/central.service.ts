import { Injectable } from '@angular/core';
import {HttpClient, HttpEvent, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CentralService {
  private readonly baseUrl = 'http://localhost:5000/antipyttern';

  constructor(private http: HttpClient) {}


  scanFiles(files: File[], pattern?: string): Observable<any> {
    const formData = new FormData();

    for (const file of files) {
      formData.append('files', file, file.webkitRelativePath || file.name);
    }

    // @ts-ignore
    const url = `${this.baseUrl}/scan_files?pattern=${encodeURIComponent(pattern)}`;
    return this.http.post(url, formData);
  }


  scanGithubRepo(repoUrl: string, pattern?: string): Observable<any> {
    // @ts-ignore
    const url = `${this.baseUrl}/scan_repo?pattern=${encodeURIComponent(pattern)}`;
    const body = { repo_url: repoUrl };

    return this.http.post(url, body);
  }

}
