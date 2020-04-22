import { Component, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { ThemeService } from '../../../services/theme.service';

@Component({
  selector: 'app-layout-main',
  templateUrl: './layout-main.component.html',
  styleUrls: [ './layout-main.component.scss'],
  encapsulation: ViewEncapsulation.None
})

export class LayoutMainComponent implements OnInit {
  isDark: boolean = false;

  constructor(private themeSvc: ThemeService) {
    this.isDark = themeSvc.getStoredTheme();
  }

  @ViewChild('drawer', { static: false }) 
  drawer: MatSidenav;

  setTheme(event){
    this.themeSvc.storeTheme(event.checked);
  }
  
  ngOnInit(): void {
  }
}