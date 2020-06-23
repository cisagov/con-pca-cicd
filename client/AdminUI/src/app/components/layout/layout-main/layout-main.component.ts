import {
  Component,
  OnInit,
  ViewChild,
  ViewEncapsulation,
  HostListener
} from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { ThemeService } from '../../../services/theme.service';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { UserAuthService } from '../../../services/user-auth.service'
import { Subscription, BehaviorSubject } from 'rxjs'

@Component({
  selector: 'app-layout-main',
  templateUrl: './layout-main.component.html',
  styleUrls: ['./layout-main.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class LayoutMainComponent implements OnInit {
  isDark: boolean = false;
  currentUserName: string = "N/A";

  constructor(
    private themeSvc: ThemeService,
    public layoutSvc: LayoutMainService,
    private userAuthSvc: UserAuthService, 
  ) {
    this.isDark = themeSvc.getStoredTheme();
    this.userAuthSvc.getUserNameBehaviorSubject().subscribe(value => {      
      this.currentUserName = value      
    })
  }

  @ViewChild('drawer', { static: false })
  drawer: MatSidenav;
  @ViewChild('mainContent', { static: false })
  mainContent;

  setTheme(event) {
    this.themeSvc.storeTheme(event.checked);
  }

  logOut(){
    this.userAuthSvc.signOut()
  }

  ngOnInit(): void {
  }

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
