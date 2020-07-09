import { Component, OnInit,Input } from '@angular/core';
import { SubscriptionService } from 'src/app/services/subscription.service';
import * as moment from 'node_modules/moment/moment';
import {
    Subscription,
    GoPhishCampaignModel,
    TimelineItem
  } from 'src/app/models/subscription.model';
  import {
    FormGroup,
    FormControl,
    FormBuilder,
    Validators,
  } from '@angular/forms';
  import { isSameDate } from 'src/app/helper/utilities';

@Component({
  selector: 'subscription-stats-tab',
  templateUrl: './subscription-stats-tab.component.html',
  styleUrls: ['./subscription-stats-tab.component.scss'] 
})
export class SubscriptionStatsTab implements OnInit {

//   @Input()
//   subscription: Subscription

    subscription: Subscription;
    selectedCycle: any;
    timelineItems: any[] = [];
    reportedStatsForm: FormGroup;
    invalidDateTimeObject: String;

  constructor(
      public subscriptionSvc: SubscriptionService
      ) {
          this.subscription = new Subscription()
      }

  ngOnInit() {
      this.subscriptionSvc.getSubBehaviorSubject().subscribe(data => {
          this.subscription = data
          if("gophish_campaign_list" in data){
            this.buildSubscriptionTimeline(this.subscription);
            this.subscription = data
            //@ts-ignore
            this.selectedCycle = this.subscription.cycles[0]
          }
        })
        this.reportedStatsForm = new FormGroup({
            reportedItems: new FormControl('', [this.invalidReportCsv]),
            overRiderNumber: new FormControl('',[Validators.pattern("^[0-9]*$")])           
          },
            { updateOn: 'blur' });
        this.invalidDateTimeObject = ""
  }

  cycleChange(event){
      console.log("cycle period changed, select new values for reporting")
      console.log(event.value)
  }

  buildSubscriptionTimeline(s: Subscription) {
    const items: TimelineItem[] = [];

    items.push({
      title: 'Subscription Started',
      date: moment(s.start_date)
    });
    // now extract a simple timeline based on campaign events
    s.gophish_campaign_list.forEach((c: GoPhishCampaignModel) => {
      for (const t of c.timeline) {
        // ignore campaigns started on the subscription start date
        if (
          t.message.toLowerCase() === 'campaign created' &&
          isSameDate(t.time, s.start_date)
        ) {
          continue;
        }

        // ignore extra campaign starts we have already put into the list
        if (
          t.message.toLowerCase() === 'campaign created' &&
          items.find(x => isSameDate(x.date, t.time)) !== null
        ) {
          continue;
        }

        if (t.message.toLowerCase() === 'campaign created') {
          items.push({
            title: 'Cycle Start',
            date: moment(t.time)
          });
        }
      }
    });

    // add an item for 'today'
    items.push({
      title: 'Today',
      date: moment()
    });

    items.push({
      title: 'Cycle End',
      date: moment(s.end_date)
    });

    this.timelineItems = items;
  }

  invalidReportCsv(control: FormControl) {
    const exprEmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const lines = control.value.split('\n');
    for (const line of lines) {
      const parts = line.split(',');
      if (parts.length !== 2) {
        return { invalidTargetCsv: true };
      }

      if (!!parts[0] && !exprEmail.test(String(parts[0]).toLowerCase())) {
        return { invalidEmailFormat: true };
      }
      if(!!parts[1]){
        let date = new Date(parts[1])
        console.log(date)
        if(isNaN(date.valueOf())){
          console.log(String(parts[1]))
          this.test("asd")
          // this.invalidDateTimeObject = "ASda"//new String(parts[1])
          return { invalidDateFormat: true}     
        }   
      }
    }

    return null;
  }
  public test(input){
    console.log(input)
  }
  get f() {
    return this.reportedStatsForm.controls;
  }

  focusOffReportList(){
    this.reportedStatsForm.updateValueAndValidity();
    console.log("focus lost")
  }

}