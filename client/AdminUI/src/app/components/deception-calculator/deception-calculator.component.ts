import { Component, OnInit, ViewChild } from '@angular/core';
import {
  FormControl,
  NgForm,
  FormGroupDirective,
  Validators,
  FormGroup,
  FormBuilder
} from '@angular/forms';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { MyErrorStateMatcher } from 'src/app/helper/ErrorStateMatcher';
import { DeceptionCalculatorService } from 'src/app/services/deception-calculator.service';
import { DeceptionCalculation } from 'src/app/models/deception-calculator.model';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { Subscription, Observable } from 'rxjs';

@Component({
  selector: 'deception-calculator',
  templateUrl: './deception-calculator.component.html',
  styleUrls: ['./deception-calculator.component.scss']
})
export class DeceptionCalculatorComponent implements OnInit {
  //models
  decpeption_calculation: DeceptionCalculation;

  //Forms and presentation elements
  templateId: string;
  deceptionFormGroup: FormGroup;
  emailPreivew: string;

  //Subscriptions
  subscriptions = Array<Subscription>();

  constructor(
    public deceptionService: DeceptionCalculatorService,
    private layoutSvc: LayoutMainService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router
  ) {
    layoutSvc.setTitle('Deception Calculator');
  }

  ngOnInit(): void {
    // this.deception_calc_obs = this.route.paramMap.pipe(
    //     switchMap((params: ParamMap) =>
    //         this.deceptionService.getBaseDeceptionCalculation(params.get('templateID'))
    //     )
    // );
    this.subscriptions.push(
      this.route.params.subscribe(params => {
        this.templateId = params['templateId'];
        if (this.templateId != undefined) {
          this.decpeption_calculation = this.deceptionService.getBaseDeceptionCalculation(
            this.templateId
          );
          this.deceptionFormGroup = this.setDeceptionFormFromModel(
            this.decpeption_calculation
          );
          this.emailPreivew = this.deceptionService.getEmailPreview(
            this.templateId
          );
        } else {
          this.router.navigate(['/templatemanager']);
        }
      })
    );
    this.subscriptions.push(
      this.layoutSvc
        .getSideNavIsSet()
        .subscribe(sideNavEmit => this.layoutSvc.closeSideNav())
    );

    this.onValueChanges();
  }

  ngOnDestroy() {
    this.subscriptions.forEach(sub => {
      sub.unsubscribe();
    });
  }

  ngAfterViewInit() {}

  saveDeceptionCalculation() {
    console.log('Data to Save :');
    console.log(this.decpeption_calculation);
    //this.deceptionService.save(this.decpeption_calculation)
  }

  onValueChanges(): void {
    this.deceptionFormGroup.valueChanges.subscribe(val => {
      //Convert form to model and save

      this.decpeption_calculation = this.getDeceptionModelFromForm(
        this.deceptionFormGroup
      );
      this.deceptionService.updateDeceptionScore(this.decpeption_calculation);

      //call save method here if saving on change
      //this.deceptionService.save(this.decpeption_calculation)

      //Update deception total score in the form for display
      this.deceptionFormGroup.patchValue(
        {
          final_deception_score: this.decpeption_calculation
            .final_deception_score
        },
        { emitEvent: false }
      );
    });
  }

  //Helper method if further csv/string cleaning is needed
  csvToArray(inputCSV: string) {
    return inputCSV.split(',');
  }

  /**
   * Set the angular form data from the provided DeceptionCalculation model
   */
  setDeceptionFormFromModel(decep_calc_model: DeceptionCalculation) {
    var csv = '';
    decep_calc_model.additional_word_tags.forEach(item => {
      csv += item + ',';
    });
    csv = csv.slice(0, -1);
    return new FormGroup({
      authoritative: new FormControl(decep_calc_model.authoritative),
      grammar: new FormControl(decep_calc_model.grammar),
      internal: new FormControl(decep_calc_model.internal),
      link_domain: new FormControl(decep_calc_model.link_domain),
      logo_graphics: new FormControl(decep_calc_model.logo_graphics),
      sender_external: new FormControl(decep_calc_model.sender_external),
      relevancy_organization: new FormControl(
        decep_calc_model.relevancy_organization
      ),
      public_news: new FormControl(decep_calc_model.public_news),
      behavior_fear: new FormControl(decep_calc_model.behavior_fear),
      duty_obligation: new FormControl(decep_calc_model.duty_obligation),
      curiosity: new FormControl(decep_calc_model.curiosity),
      greed: new FormControl(decep_calc_model.greed),
      additional_word_tags: new FormControl(csv, { updateOn: 'blur' }),
      //final_deception_score: new FormControl({value: decep_calc_model.final_deception_score, disabled:true}),
      final_deception_score: new FormControl(
        decep_calc_model.final_deception_score
      )
    });
  }

  /**
   * Get the deception calculation model from the suppied form
   */
  getDeceptionModelFromForm(decep_form: FormGroup) {
    if (this.deceptionFormGroup.valid) {
      var decep_model: DeceptionCalculation = {
        grammar: this.deceptionFormGroup.controls['grammar'].value,
        internal: this.deceptionFormGroup.controls['internal'].value,
        authoritative: this.deceptionFormGroup.controls['authoritative'].value,
        link_domain: this.deceptionFormGroup.controls['link_domain'].value,
        logo_graphics: this.deceptionFormGroup.controls['logo_graphics'].value,
        sender_external: this.deceptionFormGroup.controls['sender_external']
          .value,
        relevancy_organization: this.deceptionFormGroup.controls[
          'relevancy_organization'
        ].value,
        public_news: this.deceptionFormGroup.controls['public_news'].value,
        behavior_fear: this.deceptionFormGroup.controls['behavior_fear'].value,
        duty_obligation: this.deceptionFormGroup.controls['duty_obligation']
          .value,
        curiosity: this.deceptionFormGroup.controls['curiosity'].value,
        greed: this.deceptionFormGroup.controls['greed'].value,
        additional_word_tags: this.deceptionFormGroup.controls[
          'additional_word_tags'
        ].value.csvToArray(),
        final_deception_score: this.deceptionFormGroup.controls[
          'final_deception_score'
        ].value
      };
      return decep_model;
    } else {
      //console.log(this.deceptionFormGroup.errors);
      return;
    }
  }

  /**
   * Called to save and redirect to proper page
   */
  saveAndReturn() {
    this.saveDeceptionCalculation();

    this.router.navigate(['/templatemanager', this.templateId]);
  }
}
