import { Component } from '@angular/core';
import { FlipCardComponent} from "../../shared/flip-card/flip-card.component";

@Component({
  selector: 'app-specification',
  standalone: true,
  imports: [
    FlipCardComponent
  ],
  templateUrl: './specification.component.html',
  styleUrl: './specification.component.css'
})
export class SpecificationComponent {

}
