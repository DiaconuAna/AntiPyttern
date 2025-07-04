import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CentralService } from "../../services/central.service";
import { FormsModule } from "@angular/forms";
import { AnalysisResultService } from "../../services/analysis-result.service";
import { Router } from '@angular/router';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-detection',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './detection.component.html',
  styleUrl: './detection.component.css'
})
export class DetectionComponent {
  private selectedFiles: File[] = [];
  selectedDefect: string = 'all';
  githubRepoUrl: string = '';

  constructor(private service: CentralService, private analysisResultService: AnalysisResultService, private router: Router) {}

    onFilesSelected(event: Event): void {
      const input = event.target as HTMLInputElement;
      if (!input.files || input.files.length === 0) return;

    this.selectedFiles = Array.from(input.files);
    console.log('Files stored, waiting for scan button...');
    this.selectedFiles.forEach(file => {
      console.log('Selected:', file.webkitRelativePath || file.name);
    });
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'Upload complete',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true
    });
  }

  onScanClicked(singleFileInput: HTMLInputElement, folderInput: HTMLInputElement) {

    if (this.githubRepoUrl?.trim()) {

      Swal.fire({
        title: 'Scanning...',
        text: 'Your files are being analyzed.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
          Swal.showLoading();
        }
      });

      this.service.scanGithubRepo(this.githubRepoUrl, this.selectedDefect).subscribe({
        next: (res) => {
          Swal.close();
          this.analysisResultService.setResult(res);
          Swal.fire({
            icon: 'success',
            title: 'Scan complete!',
            text: 'GitHub repository scanned successfully.'
          });
          this.router.navigate(['/results']);
        },
        error: (err) => {
          Swal.close();
          Swal.fire({
            icon: 'error',
            title: 'Scan failed!',
            text: 'Something went wrong while scanning the repository.'
          });
          console.error('Repo scan error:', err);
        }
      });
      return;
    }


    if (this.selectedFiles.length === 0) {
      Swal.close();
      Swal.fire({
        icon: 'warning',
        title: 'No input provided',
        text: 'Please enter a GitHub repo or upload files.'
      });
      return;
    }

    Swal.fire({
      title: 'Scanning...',
      text: 'Your files are being analyzed.',
      allowOutsideClick: false,
      allowEscapeKey: false,
      didOpen: () => {
        Swal.showLoading();
      }
    });

    this.service.scanFiles(this.selectedFiles, this.selectedDefect).subscribe({
      next: res => {
        Swal.close();
        this.selectedFiles = [];
        singleFileInput.value = '';
        folderInput.value = '';
        this.analysisResultService.setResult(res);
        console.log(res)
        Swal.fire({
          icon: 'success',
          title: 'Scan complete!',
          text: 'Files have been scanned successfully.'
        });
        this.router.navigate(['/results']);
      },
      error: err => {
        Swal.close();
        Swal.fire({
          icon: 'error',
          title: 'Scan failed!',
          text: 'Something went wrong during file upload.'
        });
        console.error('Upload error:', err);
      }
    });
  }
}
