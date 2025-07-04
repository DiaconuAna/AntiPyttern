import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './core/navbar/navbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, FormsModule],
  template: `
    <app-navbar></app-navbar>
    <main class="p-6">
      <router-outlet></router-outlet>
    </main>
  `
})
export class AppComponent {}
