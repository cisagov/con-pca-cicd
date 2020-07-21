import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AppSettings } from 'src/app/AppSettings';
import { ReportsService } from 'src/app/services/reports.service';

@Component({
  selector: 'app-yearly',
  templateUrl: './yearly.component.html',
  styleUrls: ['./yearly.component.scss']
})
export class YearlyComponent implements OnInit {

  private routeSub: any;
  subscriptionUuid: string;
  reportStartDate: Date;
  detail: any;

  dateFormat = AppSettings.DATE_FORMAT;

  /**
   *
   */
  constructor(
    public reportsSvc: ReportsService,
    private route: ActivatedRoute,
  ) { }

  /**
   *
   */
  ngOnInit(): void {
    this.routeSub = this.route.params.subscribe(params => {
      this.subscriptionUuid = params.id;
      let isDate = new Date(params.start_date)
      const isLocal = params.local;
  
      if(isDate.getTime()){
        this.reportStartDate = isDate
      } else {
        console.log("Invalid Date time provided, defaulting to now")
        this.reportStartDate = new Date()        
      }

      if(isLocal){
        this.reportsSvc.getCycleReportLocal(this.subscriptionUuid, this.reportStartDate).subscribe(resp => {
          this.detail = resp;
          this.renderReport();
        });
      }else{
        this.reportsSvc.getCycleReport(this.subscriptionUuid, this.reportStartDate).subscribe(resp => {
          this.detail = resp;
          this.renderReport();
        });
      }      
    });
  }

  /**
   *
   */
  renderReport() {

  }
}
