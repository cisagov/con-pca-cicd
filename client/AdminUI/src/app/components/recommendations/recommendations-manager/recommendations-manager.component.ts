import {
    Component,
    OnInit,
    Input,
    OnDestroy,
    Inject,
    ChangeDetectionStrategy
} from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { MyErrorStateMatcher } from '../../../helper/ErrorStateMatcher';
import { Recommendations } from 'src/app/models/recommendations.model';
import { Router, ActivatedRoute } from '@angular/router';
import { RecommendationsService } from 'src/app/services/recommendations.service';
import {
    MatDialog,
    MAT_DIALOG_DATA,
    MatDialogRef
} from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { Subscription } from 'rxjs';

@Component({
    selector: 'app-recommendations-manager',
    templateUrl: './recommendations-manager.component.html',
    styleUrls: ['./recommendations-manager.component.html'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class RecommendationsManagerComponent implements OnInit, OnDestroy {
    @Input() inDialog: boolean;

    // List of angular subscriptions, unsubscribed to on delete
    angularSubscriptions = Array<Subscription>();
    // Customer_uuid if not new
    recommendations_uuid: string;
    customer: Recommendations;

    constructor(
        public recommendationsSvc: RecommendationsService,
        public dialog: MatDialog,
        private route: ActivatedRoute,
        public router: Router,
        public layoutSvc: LayoutMainService
    ) {
        layoutSvc.setTitle('Recommendations Manager');
    }

    ngOnInit(): void {
        if (this.dialog.openDialogs.length > 0) {
            this.inDialog = true;
        } else {
            this.inDialog = false;
        }
    }

    ngOnDestroy() {
        // Unsubscribe from all subscriptions
        this.angularSubscriptions.forEach(sub => {
            sub.unsubscribe();
        });
    }
}
