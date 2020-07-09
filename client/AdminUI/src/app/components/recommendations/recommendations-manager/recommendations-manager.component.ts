import {
    Component,
    Input,
} from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { MyErrorStateMatcher } from '../../../helper/ErrorStateMatcher';
import { Recommendations } from 'src/app/models/recommendations.model';
import { Router } from '@angular/router';
import { RecommendationsService } from 'src/app/services/recommendations.service';
import { LayoutMainService } from 'src/app/services/layout-main.service';

@Component({
    selector: 'app-recommendations-manager',
    templateUrl: './recommendations-manager.component.html',
    styleUrls: ['./recommendations-manager.component.scss'],
})

export class RecommendationsManagerComponent {

    recommendations_uuid: string;
    recommendations: Recommendations;

    constructor(
        public recommendationsSvc: RecommendationsService,
        public router: Router,
        public layoutSvc: LayoutMainService
    ) {
        layoutSvc.setTitle('Recommendations Manager');
    }

    pushRecommendations() {
        this.recommendationsSvc.saveNewRecommendation(this.recommendations).subscribe(
            (data: any) => {
                this.router.navigate(['/recommendations']);
            }
        )
    }
}
