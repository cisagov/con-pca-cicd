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

  //Update the final deception score of the provided DeceptionCalculation model
  getAllTemplates() {
    // return this.http.get('http://localhost:8000/api/v1/templates/list', headers);
    var template_list = [];
    for (var i = 0; i < 40; i++) {
      template_list.push(
        new TemplateShort({
          template_uuid: 'uuid - ' + i,
          name: 'Template Name - ' + i,
          descriptive_words: this.getDescriptiveWords(i)
        })
      );
    }
    return template_list;
  }

  getTemlpate(uuid: string) {
    // return this.http.get('http://localhost:8000/api/v1/template/{{uuid}}', headers);
    var retVal = new Template({
      name: 'Test Template : ' + uuid.split(' ')[2],
      template_uuid: uuid,
      subject: 'Email Subject',
      text:
        `
            <h1> Email Header ` +
        uuid.split(' ')[2] +
        ` </h1>
            <b>Dear Email Reader </b>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. </p>
            `,
      description: 'Example Description ' + uuid,
      from_address: 'From@Address' + uuid + '.com',
      descriptive_words: [
        'Descriptive',
        'Items',
        'Email',
        'Phishing',
        'Secret',
        'Array'
      ]
    });
    return retVal;
  }

  saveTemplate(template: Template) {
    return new Promise((resolve, reject) => {
      // this.http.post('http://localhost:8000/api/v1/template/{{uuid}}',template)
      // .subscribe(
      //     (success) => {
      //         console.log("Saved template successfully")
      //         resolve("Template Saved")
      //     },
      //     (error) => {
      //         console.log("Error saving template")
      //         console.log(error)
      //         reject("Template could not save")
      //     },
      //     () => {
      //         console.log("Post obeservable complete")
      //     });

      //TESTING
      if (!template.template_uuid) {
        resolve('NEW TEMPLATE CREATED');
      }
      if (template.template_uuid.length % 2 == 0) {
        reject('UUID even length');
      } else {
        resolve('UUID odd length');
      }
    });
  }

  //testing method
  getDescriptiveWords(seed: number) {
    var retVal = [];
    if (seed == 1) {
      retVal.push('First');
    }
    if (seed % 2 == 0) {
      retVal.push('Test');
    }
    if (seed % 3 == 0) {
      retVal.push('Three');
    }
    if (seed % 3 == 0) {
      retVal.push('Important');
    }
    return retVal;
  }
}
