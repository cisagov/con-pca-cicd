import {
    Component,
    Input,
    OnInit,
} from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { MyErrorStateMatcher } from '../../../helper/ErrorStateMatcher';
import { Recommendations } from 'src/app/models/recommendations.model';
import { Router, ActivatedRoute } from '@angular/router';
import { RecommendationsService } from 'src/app/services/recommendations.service';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { AlertComponent } from '../../dialogs/alert/alert.component';
import { MatDialog } from '@angular/material/dialog';
import { Subscription } from 'rxjs';

@Component({
    selector: 'app-recommendations-manager',
    templateUrl: './recommendations-manager.component.html',
    styleUrls: ['./recommendations-manager.component.scss'],
})

export class RecommendationsManagerComponent implements OnInit {

    recommendationsId: string;
    recommendations: Recommendations;
    recommendationsFormGroup: FormGroup;
    subscriptions = Array<Subscription>();

    constructor(
        public recommendationsSvc: RecommendationsService,
        private route: ActivatedRoute,
        public router: Router,
        public layoutSvc: LayoutMainService,
        public dialog: MatDialog
    ) {
        layoutSvc.setTitle('Recommendations Manager');
        this.setRecommendationsForm(new Recommendations())
    }


    ngOnInit(): void {
        this.route.params.subscribe(params => {
            this.recommendationsId = params["recommendationsId"];
            if (this.recommendationsId != undefined) {
                this.subscriptions.push(
                    this.recommendationsSvc.getRecommendation(this.recommendationsId).subscribe(
                        (recommendationsData: Recommendations) => {
                            this.recommendationsId = recommendationsData.recommendations_uuid;
                            this.setRecommendationsForm(recommendationsData)
                        }
                    )
                )
            }
        })
    }

    ngOnDestroy() {
        this.subscriptions.forEach(sub => {
            sub.unsubscribe();
        });
    }

    //Create a formgroup using a Template as initial data
    setRecommendationsForm(recommendation: Recommendations) {

        if (!recommendation.appearance) {
            recommendation.appearance = <any>{};
        }
        if (!recommendation.sender) {
            recommendation.sender = <any>{};
        }
        if (!recommendation.relevancy) {
            recommendation.relevancy = <any>{};
        }
        if (!recommendation.behavior) {
            recommendation.behavior = <any>{};
        }

        this.recommendationsFormGroup = new FormGroup({
            recommendationsUUID: new FormControl(recommendation.recommendations_uuid),
            recommendationsName: new FormControl(recommendation.name, [Validators.required]),
            recommendationsDeceptionLevel: new FormControl(recommendation.deception_level),
            recommendationsDescription: new FormControl(recommendation.description),
            authoritative: new FormControl(recommendation.sender?.authoritative ?? 0),
            external: new FormControl(recommendation.sender?.external ?? 0),
            internal: new FormControl(recommendation.sender?.internal ?? 0),
            grammar: new FormControl(recommendation.appearance?.grammar ?? 0),
            link_domain: new FormControl(recommendation.appearance?.link_domain ?? 0),
            logo_graphics: new FormControl(recommendation.appearance?.logo_graphics ?? 0),
            organization: new FormControl(recommendation.relevancy?.organization ?? 0),
            public_news: new FormControl(recommendation.relevancy?.public_news ?? 0),
            fear: new FormControl(recommendation.behavior?.fear ?? false),
            duty_obligation: new FormControl(
                recommendation.behavior?.duty_obligation ?? false
            ),
            curiosity: new FormControl(recommendation.behavior?.curiosity ?? false),
            greed: new FormControl(recommendation.behavior?.greed ?? false),
        });
    }

    saveRecommendations() {
        if (this.recommendationsFormGroup.valid) {
            let template_to_save = this.getRecommendationsModelFromForm(
                this.recommendationsFormGroup
            );
            if (this.recommendationsId) {
                this.recommendationsSvc.saveNewRecommendation(template_to_save);
            } else {
                this.recommendationsSvc.saveNewRecommendation(template_to_save);
            }
        } else {
            this.dialog.open(AlertComponent, {
                data: {
                    title: 'Error',
                    messageText: 'Errors on deception form' + this.recommendationsFormGroup.errors
                }
            });
        }
    }

    /**
     * Returns a Recommendation model initialized from a provided formgroup
     * @param decep_form
     */
    getRecommendationsModelFromForm(decep_form: FormGroup) {
        let formRecommendations = new Recommendations(decep_form.value);
        let saveRecommendations = new Recommendations();
        saveRecommendations.appearance = {
            grammar: formRecommendations.grammar,
            link_domain: formRecommendations.link_domain,
            logo_graphics: formRecommendations.logo_graphics
        };
        saveRecommendations.sender = {
            authoritative: formRecommendations.authoritative,
            external: formRecommendations.external,
            internal: formRecommendations.internal
        };
        saveRecommendations.relevancy = {
            organization: formRecommendations.organization,
            public_news: formRecommendations.public_news
        };
        saveRecommendations.behavior = {
            curiosity: formRecommendations.curiosity,
            duty_obligation: formRecommendations.duty_obligation,
            fear: formRecommendations.fear,
            greed: formRecommendations.greed
        };
        saveRecommendations.recommendations_uuid = this.recommendationsId;
        return saveRecommendations;
    }

    pushRecommendations() {
        this.recommendationsSvc.saveNewRecommendation(this.recommendations).subscribe(
            (data: any) => {
                this.saveRecommendations();
                this.router.navigate(['/recommendations']);
            },
            (error) => {
                console.log(error)
            }
        )
    }
}
