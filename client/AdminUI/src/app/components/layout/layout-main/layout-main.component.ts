import {
  Component,
  OnInit,
  ViewChild,
  ViewEncapsulation,
  HostListener
} from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { OverlayContainer } from '@angular/cdk/overlay';
import { ThemeService } from '../../../services/theme.service';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-layout-main',
  templateUrl: './layout-main.component.html',
  styleUrls: ['./layout-main.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class LayoutMainComponent implements OnInit {
  isDark: boolean = false;
  username: string = '';

  constructor(
    private themeSvc: ThemeService,
    public layoutSvc: LayoutMainService, 
    public userSvc: UserService, 
    public overlayContainer: OverlayContainer
  ) {
    this.isDark = themeSvc.getStoredTheme();
    this.username = userSvc.getCurrentUser();
    if(this.isDark){
      overlayContainer.getContainerElement().classList.add('theme-alternate');
    } 
  }

  @ViewChild('drawer', { static: false })
  drawer: MatSidenav;
  @ViewChild('mainContent', { static: false })
  mainContent;

  setTheme(event) {
    this.themeSvc.storeTheme(event.checked);
    this.isDark = event.checked;
    if(event.checked){
      this.overlayContainer.getContainerElement().classList.add('theme-alternate');
    } else {
      this.overlayContainer.getContainerElement().classList.remove('theme-alternate');
    }
  }

  ngOnInit(): void {}

  ngAfterViewInit() {
    setTimeout(() => {
      this.setContentHeight();
    });
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.setContentHeight();
  }

  setContentHeight() {
    //TODO get values of card padding
    let default_card_padding = 16;
    let default_card_margin = 10;
    this.layoutSvc.setContentHeight(
      this.mainContent.elementRef.nativeElement.offsetHeight -
        default_card_margin * 2 -
        default_card_padding * 2
    );
  }
}
