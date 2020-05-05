import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DeceptionCalculation } from 'src/app/models/deception-calculator.model';
import { Template } from 'src/app/models/template.model'
import { templateJitUrl } from '@angular/compiler';
import { Observable } from 'rxjs';

const headers = {
  headers: new HttpHeaders().set('Content-Type', 'application/json'),
  params: new HttpParams()
};

@Injectable()
export class DeceptionCalculatorService {
  constructor(private http: HttpClient) {}

  getDeception(templateUUID: string){
    return this.http.get(
      `http://localhost:8000/api/v1/template/${templateUUID}`,
      headers
    );
  }

  //Update the final deception score of the provided DeceptionCalculation model
  updateDeceptionScore(deception_calculation: DeceptionCalculation) {
    return
      deception_calculation.authoritative +
      deception_calculation.grammar +
      deception_calculation.internal +
      deception_calculation.link_domain +
      deception_calculation.logo_graphics +
      deception_calculation.public_news +
      deception_calculation.relevancy_organization +
      deception_calculation.sender_external;
  }
  
  deceptionModelFromTemplate(template: Template){

    let retVal: DeceptionCalculation = new DeceptionCalculation()

    //Template Display Contents
    retVal.temlpateName = template.name
    retVal.templateBody = template.html
    retVal.templateSubject = template.subject

    //Deception Calc Components
    retVal.grammar = template.appearance.grammar
    retVal.link_domain = template.appearance.link_domain
    retVal.logo_graphics = template.appearance.logo_graphics
    retVal.sender_external = template.sender.external
    retVal.internal = template.sender.internal
    retVal.authoritative = template.sender.authoritative
    retVal.relevancy_organization = template.relevancy.organization
    retVal.public_news = template.relevancy.public_news
    retVal.behavior_fear = !!template.behavior.fear
    retVal.duty_obligation = !!template.behavior.duty_obligation
    retVal.curiosity = !!template.behavior.curiosity
    retVal.greed = !!template.behavior.greed
    retVal.final_deception_score = template.deception_score

    return retVal

  }

  //Testing method
  //Get a blank DeceptionCalculation model for form population
  getBaseDeceptionCalculation(templateUUID: string) {
    console.log('Attempting to open template with UUID : ', templateUUID);
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
    decep_calc.additional_word_tags = "Test, Values, Here";

    this.updateDeceptionScore(decep_calc);

    return decep_calc;
  }

  //Testing Method
  //Get a Html formatted string for display
  getEmailPreview(templateId: string) {
    console.log('retreiving email preview for template' + templateId);
    //var email_preview = return this.http.get('http://localhost:8000/api/v1/ EMAIL URL HERE /', headers);
    var email_preview = `
            <h1> Email Header </h1>
            <b>Dear Email Reader </b>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. </p>
            <p>"Sed ut <a href="#">perspiciatis</a> unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. </p>
            <p>"Sed ut <a href="#">perspiciatis</a> unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. </p>
            <p>"Sed ut <a href="#">perspiciatis</a> unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"</p>

            <p> Regards </p>
            <p> Test Email Team </p>
        `;
    return email_preview;
  }

  // getDeception(){
  //     //return this.http.get('http://localhost:8000/api/v1/deception-calculator/', headers);
  // }

  // updatePreiview(){

  // }
}
