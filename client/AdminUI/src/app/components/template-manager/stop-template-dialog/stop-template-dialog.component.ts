import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Template } from 'src/app/models/template.model';
import { SubscriptionService } from 'src/app/services/subscription.service';
import { Subscription } from 'src/app/models/subscription.model';
import { TemplateManagerService } from 'src/app/services/template-manager.service';

@Component({
  selector: 'app-stop-template-dialog',
  templateUrl: './stop-template-dialog.component.html',
  styleUrls: ['../template-manager.component.scss']
})
export class StopTemplateDialogComponent implements OnInit {
  template: Template
  subscriptions: Subscription[]

  displayedColumns = [
    "subscription_name"
  ]
  constructor(
    public dialogRef: MatDialogRef<StopTemplateDialogComponent>,
    public subscriptionSvc: SubscriptionService,
    public templateSvc: TemplateManagerService,
    @Inject(MAT_DIALOG_DATA) data: Template) { 
      this.template = data
    }

  ngOnInit(): void {
    this.subscriptionSvc.getSubscriptionsByTemplate(this.template).subscribe((data: any[]) => {
      this.subscriptions = data as Subscription[]
    })
  }

  confirm(): void {
    if(window.confirm(`Are you sure you want to stop the subscriptions?`)) {
      this.templateSvc.stopTemplate(this.template)
      this.dialogRef.close()
    } else {
      this.dialogRef.close()
    }
  }

  cancel(): void {
    this.dialogRef.close()
  }

  onNoClick(): void {
    this.dialogRef.close()
  }
}
