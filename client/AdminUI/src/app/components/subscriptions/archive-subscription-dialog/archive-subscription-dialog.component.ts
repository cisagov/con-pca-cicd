import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Subscription } from 'src/app/models/subscription.model';
import { SubscriptionService } from 'src/app/services/subscription.service';

@Component({
  selector: 'app-archive-subscription-dialog',
  templateUrl: './archive-subscription-dialog.component.html',
  styleUrls: ['./archive-subscription-dialog.component.scss']
})
export class ArchiveSubscriptionDialogComponent implements OnInit {
  subscription: Subscription

  constructor(
    public dialogRef: MatDialogRef<ArchiveSubscriptionDialogComponent>,
    public subscriptionSvc: SubscriptionService,
    @Inject(MAT_DIALOG_DATA) data: Subscription) { 
      this.subscription = data
    }

  ngOnInit(): void {
  }

  cancel(): void {
    this.dialogRef.close()
  }

  archive(): void {
    this.subscription.archived = true
    this.subscriptionSvc.patchSubscription(this.subscription).subscribe((data: any) => {
      this.dialogRef.close()
    })
  }
}
