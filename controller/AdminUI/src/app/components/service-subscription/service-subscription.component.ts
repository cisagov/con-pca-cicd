import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { AddOrganizationComponent} from '../../components/organization/add-organization/add-organization.component';

@Component({
  selector: 'app-service-subscription',
  templateUrl: './service-subscription.component.html', 
  styleUrls: ['./service-subscription.component.scss'],
  directives: [ AddOrganizationComponent ] 
})
export class ServiceSubscriptionComponent implements OnInit {
   
  constructor() { }

  ngOnInit(): void {
  }

}