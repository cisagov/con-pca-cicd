import { Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { Router } from "@angular/router";

@Injectable()
export class DashboardService {
  
  private apiUrl: string;
  constructor(private http: HttpClient, private router: Router) {}
}
