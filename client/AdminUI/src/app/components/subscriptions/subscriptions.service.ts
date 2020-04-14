import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from "@angular/core";
import { Router } from "@angular/router";

const headers = {
   headers: new HttpHeaders()
     .set('Content-Type', 'application/json'),
   params: new HttpParams()
 };

@Injectable()
export class SubscriptionsService {
   constructor(private http: HttpClient) {}

   getSubscriptionsData(){
      return this.http.get('http://localhost:8000/api/v1/subscriptions/', headers);
    }
}
