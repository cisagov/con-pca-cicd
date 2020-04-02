import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-layout-main',
  templateUrl: './layout-main.component.html',
  styleUrls: [ './layout-main.component.scss' ]
})
export class LayoutMainComponent implements OnInit {

  constructor() {
  }

  @ViewChild('drawer', { static: false }) 
  drawer: MatSidenav;

  ngOnInit(): void {
  }
}