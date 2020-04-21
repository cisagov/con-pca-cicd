import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { DeceptionCalculation } from 'src/app/models/deception-calculator.model';

const headers = {
   headers: new HttpHeaders()
     .set('Content-Type', 'application/json'),
   params: new HttpParams()
 };

@Injectable()
export class DeceptionCalculatorService {
   constructor(private http: HttpClient) {}

   //Testing method
   getBaseDeceptionCalculation(){
    var decep_calc = new DeceptionCalculation();
    
    //No score variables
    decep_calc.behavior_fear = false;
    decep_calc.curiosity = false;
    decep_calc.duty_obligation = false;
    decep_calc.greed = false;

    //Scored variables
    decep_calc.authoritative = 0;
    decep_calc.grammar = 0;
    decep_calc.internal = 0;
    decep_calc.link_domain = 0;
    decep_calc.logo_graphics = 0;
    decep_calc.public_news = 0;
    decep_calc.relevancy_organization = 0;
    decep_calc.sender_external = 0;

    //Text array
    decep_calc.additional_word_tags = ["test","values","here"];

    this.updateDeceptionScore(decep_calc)

    return decep_calc
   } 

    updateDeceptionScore(deception_calculation: DeceptionCalculation){
        deception_calculation.final_deception_score = 
            deception_calculation.authoritative + 
            deception_calculation.grammar + 
            deception_calculation.link_domain + 
            deception_calculation.logo_graphics +
            deception_calculation.public_news + 
            deception_calculation.relevancy_organization + 
            deception_calculation.sender_external
        console.log("Score Updated " + deception_calculation.final_deception_score)
   }


    // getDeception(){
    //     //return this.http.get('http://localhost:8000/api/v1/deception-calculator/', headers); 
    // }

    // updatePreiview(){

    // }

}
