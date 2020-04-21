import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, NgForm, FormGroupDirective, Validators, FormGroup, FormBuilder } from '@angular/forms';
import { MyErrorStateMatcher } from 'src/app/helper/ErrorStateMatcher';
import { DeceptionCalculatorService } from 'src/app/components/deception-calculator/deception-calculator.service';
import { DeceptionCalculation } from 'src/app/models/deception-calculator.model';
import { MatSidenav } from '@angular/material/sidenav';
import { MAT_DRAWER_CONTAINER } from '@angular/material/sidenav/drawer';

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

    @ViewChild('drawer')
    drawer: MatSidenav;


    constructor(
        public deceptionService : DeceptionCalculatorService,
        private fb: FormBuilder,
    ) { 
    }

    ngOnInit(): void {
        console.log("Deception Calculator Init Test")
        
        
        this.decpeption_calculation = this.deceptionService.getBaseDeceptionCalculation()
        this.deceptionFormGroup = this.setDeceptionFormFromModel(this.decpeption_calculation);
        this.emailPreivew = this.deceptionService.getEmailPreview();
        
        this.onValueChanges()

    }

    ngAfterViewInit(){
        
        console.log(this.drawer)
    }

    onValueChanges(): void {
        this.deceptionFormGroup.valueChanges.subscribe( val => {
            this.decpeption_calculation  =  val
            this.deceptionService.updateDeceptionScore(this.decpeption_calculation)
            //call save method here if saving on change 
            this.deceptionFormGroup.patchValue({final_deception_score: this.decpeption_calculation.final_deception_score},{emitEvent: false})
        })
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
            additional_word_tags: new FormControl(csv, {updateOn: 'blur'}),
            //final_deception_score: new FormControl({value: decep_calc_model.final_deception_score, disabled:true}),
            final_deception_score: new FormControl(decep_calc_model.final_deception_score),
        })

    }

    testingMethod(){
        console.log("testing method called")
        console.log(this.deceptionFormGroup)
    }

    

}