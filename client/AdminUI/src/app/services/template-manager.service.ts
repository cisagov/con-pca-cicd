import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Template, TemplateShort } from 'src/app/models/template.model';

const headers = {
  headers: new HttpHeaders().set('Content-Type', 'application/json'),
  params: new HttpParams()
};

@Injectable()
export class TemplateManagerService {
  constructor(private http: HttpClient) {}

  //GET a list of all templates
  getAllTemplates() {
    return this.http.get('http://localhost:8000/api/v1/templates', headers);
  }

  //GET a single template using the provided temlpate_uuid
  getTemplate(uuid: string) {
    return new Promise((resolve, reject) => {
      this.http
        .get(`http://localhost:8000/api/v1/template/${uuid}`)
        .subscribe(
          success => {
            resolve(success);
          },
          error => {
            reject(error);
          },
          () => {
          }
        );
    });
  }

  //POST a new template
  saveNewTemplate(template: Template) {
    console.log(template);
    return new Promise((resolve, reject) => {
      this.http
        .post('http://localhost:8000/api/v1/templates/', template)
        .subscribe(
          success => {
            resolve(success);
          },
          error => {
            reject(error);
          },
          () => {
          }
        );
    });
  }
  //PATCH an existing template with partial data
  updateTemplate(template: Template) {
    console.log(template);
    return new Promise((resolve, reject) => {
      this.http
        .patch(`http://localhost:8000/api/v1/template/${template.template_uuid}/`, template)
        .subscribe(
          success => {
            resolve(success);
          },
          error => {
            reject(error);
          },
          () => {
          }
        );
    });
  }
  
}
