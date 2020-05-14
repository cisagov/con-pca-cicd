import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DeceptionCalculation } from 'src/app/models/deception-calculator.model';
import { Template, TemplateAppearanceModel, TemplateSenderModel, TemplateRelevancyModel, TemplateBehaviorModel } from 'src/app/models/template.model'
import { templateJitUrl } from '@angular/compiler';
import { Observable } from 'rxjs';

const headers = {
  headers: new HttpHeaders().set('Content-Type', 'application/json'),
  params: new HttpParams()
};

@Injectable()
export class DeceptionCalculatorService {
  constructor(private http: HttpClient) {}

  //GET single template for use in the deception calculator
  getDeception(templateUUID: string){
    return this.http.get(
      `http://localhost:8000/api/v1/template/${templateUUID}`,
      headers
    );
  }

  //PATCH an updated deception calculation using the Template model
  saveDeception(template: Template){
    return new Promise((resolve, reject) => {
      this.http
        .patch(`http://localhost:8000/api/v1/template/${template.template_uuid}/`, template)
        .subscribe(
          success => {
            resolve('Template Saved');
          },
          error => {
            console.log(error);
          },
          () => {
            console.log('Post obeservable complete');
          }
        );    
      })
    }
}
