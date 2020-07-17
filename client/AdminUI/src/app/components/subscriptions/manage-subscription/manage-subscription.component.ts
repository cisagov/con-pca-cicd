import { Component, OnInit, OnDestroy } from '@angular/core';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Subscription } from 'src/app/models/subscription.model';
import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-manage-subscription',
  templateUrl: './manage-subscription.component.html',
  styleUrls: ['./manage-subscription.component.scss']
})
export class ManageSubscriptionComponent implements OnInit, OnDestroy {
 
  private routeSub: any;
  subscription: Subscription

  constructor(
    private layoutSvc: LayoutMainService,
    private subscriptionSvc: SubscriptionService,
    private route: ActivatedRoute,
    ) {
  }

  ngOnInit() {

      this.routeSub = this.route.params.subscribe(params => {
        if (!params.id) {
          //this.loadPageForCreate(params);
        } else {
          this.loadPageForEdit(params);

        }
      });
  }

  onTabChanged(event){
    window.dispatchEvent(new Event('resize'));
  }

  loadPageForEdit(params: any) {
    this.subscriptionSvc.subscription = new Subscription()
    const sub = this.subscriptionSvc.subscription;
    sub.subscription_uuid = params.id;

    this.subscriptionSvc
      .getSubscription(sub.subscription_uuid)
      .subscribe((s: Subscription) => {
        this.subscriptionSvc.setSubBhaviorSubject(s)
        this.subscription = s as Subscription;
        this.subscriptionSvc.subscription = this.subscription;
        this.setPageTitle()
      })
  }
  setPageTitle() {
    if(this.subscription){
      let title = `Edit Subscription: ${this.subscription.name}`;
      if (this.subscription.status.toLowerCase() === 'stopped') {
        title += ' (stopped)';
      }
      this.layoutSvc.setTitle(title);
    }
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }
}