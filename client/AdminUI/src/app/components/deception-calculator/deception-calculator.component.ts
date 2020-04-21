import { Component, OnInit } from '@angular/core';
import { FormControl, NgForm, FormGroupDirective, Validators, FormGroup, FormBuilder } from '@angular/forms';
import { MyErrorStateMatcher } from 'src/app/helper/ErrorStateMatcher';
import { DeceptionCalculatorService } from 'src/app/components/deception-calculator/deception-calculator.service';
import { DeceptionCalculation } from 'src/app/models/deception-calculator.model';

@Component({
  selector: 'deception-calculator',
  templateUrl: './deception-calculator.component.html',
  styleUrls: ['./deception-calculator.component.scss']
})

export class DeceptionCalculatorComponent implements OnInit {
    
    //models
    decpeption_calculation: DeceptionCalculation
    
    //Forms and presentation elements
    deceptionFormGroup: FormGroup
    emailPreivew: string

    constructor(
        public deceptionService : DeceptionCalculatorService,
        private fb: FormBuilder
    ) { 
        this.decpeption_calculation = this.deceptionService.getBaseDeceptionCalculation()
        this.deceptionFormGroup = this.setDeceptionFormFromModel(this.decpeption_calculation);
        this.emailPreivew = this.deceptionService.getEmailPreview();
    }

    ngOnInit(): void {
        console.log("Deception Calculator Init Test")
        console.log(this.deceptionFormGroup)
    }
    
    setDeceptionFormFromModel(decep_calc_model: DeceptionCalculation){
        var csv = "";
        decep_calc_model.additional_word_tags.forEach(item => {
            csv += (item + ",")
        })
        csv = csv.slice(0,-1);
        return new FormGroup({
            authoritative: new FormControl(decep_calc_model.authoritative),
            grammar: new FormControl(decep_calc_model.grammar),
            internal: new FormControl(decep_calc_model.internal),
            link_domain: new FormControl(decep_calc_model.link_domain),
            logo_graphics: new FormControl(decep_calc_model.logo_graphics),
            sender_external: new FormControl(decep_calc_model.sender_external),
            relevancy_organization: new FormControl(decep_calc_model.relevancy_organization),
            public_news: new FormControl(decep_calc_model.public_news),
            behavior_fear: new FormControl(decep_calc_model.behavior_fear),
            duty_obligation: new FormControl(decep_calc_model.duty_obligation),
            curiosity: new FormControl(decep_calc_model.curiosity),
            greed: new FormControl(decep_calc_model.greed),
            additional_word_tags: new FormControl(csv)
        })

    }

    //Used for testing purposes
    setDeceptionFormEmpty(){
        return new FormGroup({
            authoritative: new FormControl(0),
            grammar: new FormControl(0),
            internal: new FormControl(0),
            link_domain: new FormControl(0),
            logo_graphics: new FormControl(0),
            sender_external: new FormControl(0),
            relevancy_organization: new FormControl(0),
            public_news: new FormControl(0),
            behavior_fear: new FormControl(false),
            duty_obligation: new FormControl(false),
            curiosity: new FormControl(false),
            greed: new FormControl(false),
            additional_word_tags: new FormControl('')
        })
    }

    testingMethod(){
        console.log("testing method called")
        console.log(this.deceptionFormGroup)
    }

    

}