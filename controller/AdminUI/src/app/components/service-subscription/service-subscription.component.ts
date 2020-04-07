import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { AddOrganizationComponent} from '../../components/organization/add-organization/add-organization.component';

@Component({
  selector: 'app-service-subscription',
  directives: [ AddOrganizationComponent ] 
  styleUrls: ['./service-subscription.component.scss'],
  templateUrl: './service-subscription.component.html', 
})
export class ServiceSubscriptionComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}