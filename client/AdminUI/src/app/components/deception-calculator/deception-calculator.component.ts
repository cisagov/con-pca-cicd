import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'deception-calculator',
  templateUrl: './deception-calculator.component.html',
  styleUrls: ['./deception-calculator.component.scss']
})

export class DeceptionCalculatorComponent implements OnInit {

  
  constructor(
    ) { }

  ngOnInit(): void {
    //this.deceptionCalcService.getBase()
    console.log("Deception Calculator Init Test")
  }
  
}