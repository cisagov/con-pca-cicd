import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

import { Template } from 'src/app/models/template.model';

const headers = {
  headers: new HttpHeaders().set('Content-Type', 'application/json'),
  params: new HttpParams()
};

@Injectable()
export class TemplateManagerService {
  constructor(private http: HttpClient) {}

  //GET a list of all templates
  getAllTemplates() {
    return this.http.get(`${environment.apiEndpoint}/api/v1/templates`, headers);
  }

  // getAllTemplates() {
  //   return new Promise((resolve, reject) => {
  //     this.http
  //     .get('http://localhost:8000/api/v1/templates', headers)
  //     .subscribe(
  //       (success) => {
  //         return success
  //       },
  //       (error) => {
  //         return error
  //       }
  //     )
  //   })
  // }

  //GET a single template using the provided temlpate_uuid
  getTemplate(uuid: string) {
    return new Promise((resolve, reject) => {
      this.http
        .get(`${environment.apiEndpoint}/api/v1/template/${uuid}`)
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
    return new Promise((resolve, reject) => {
      this.http
        .post(`${environment.apiEndpoint}/api/v1/templates/`, template)
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
    return new Promise((resolve, reject) => {
      this.http
        .patch(`${environment.apiEndpoint}/api/v1/template/${template.template_uuid}/`, template)
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
  deleteTemplate(template: Template) {
    return new Promise((resolve,reject) => {
      this.http
      .delete(`${environment.apiEndpoint}/api/v1/template/${template.template_uuid}/`)
      .subscribe(
        success => {
          resolve(success);
        },
        error => {
          reject(error)
        }
      )
    })
  }

  stopTemplate(template: Template) {
    return this.http.get(`${environment.apiEndpoint}/api/v1/template/stop/${template.template_uuid}/`);
  }

}
