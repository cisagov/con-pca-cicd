import { SettingsService } from 'src/app/services/settings.service';
import { Component, OnInit, Input } from '@angular/core';
import { LayoutMainService } from 'src/app/services/layout-main.service';

@Component({
  selector: '',
  templateUrl: './user-admin.component.html',
  styleUrls: ['./user-admin.component.scss']
})
export class UserAdminComponent implements OnInit {
  constructor(public layoutSvc: LayoutMainService) {
    layoutSvc.setTitle('User Admin');
  }

  ngOnInit() { }

  launchFlower() {
    const url = "localhost:5555/";
    window.open(url, '_blank');
  }
}