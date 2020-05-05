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
import { Template } from 'src/app/models/template.model'
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
  templateName: string;
  templateSubject: string
  templateHTML: string;

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

    //Set formGroup to empty model to avoid collision when HTML is rendered
    this.setDeceptionFormFromModel(new DeceptionCalculation)
  }

  ngOnInit(): void {

    //Get a subscription to the template and build out the formGroup and html preview
    this.subscriptions.push(
      this.route.params.subscribe(params => {
        this.templateId = params['templateId'];
        if (this.templateId != undefined) {
          this.subscriptions.push(this.deceptionService.getDeception(this.templateId).subscribe((templateData: Template) => {
            console.log(templateData)
            let decepModel = this.deceptionService.deceptionModelFromTemplate(templateData)
            this.setDeceptionFormFromModel(decepModel)
            this.setTemplatePreview(decepModel)
            this.onValueChanges();
          }))
        } else {
          this.router.navigate(['/templatemanager']);
        }
      })
    );

    //Get access to the sidenav element, set to closed initially
    this.subscriptions.push(
      this.layoutSvc
        .getSideNavIsSet()
        .subscribe(sideNavEmit => this.layoutSvc.closeSideNav())
    );
  }

  ngOnDestroy() {
    this.subscriptions.forEach(sub => {
      sub.unsubscribe();
    });
  }

  ngAfterViewInit() {}

  saveDeceptionCalculation() {
    console.log('Data to Save :');
    this.getDeceptionModelFromForm(this.deceptionFormGroup)
    //console.log(this.decpeption_calculation);
  }

  onValueChanges(): void {
    this.deceptionFormGroup.valueChanges.subscribe(val => {
      this.deceptionFormGroup.patchValue(
        {
          final_deception_score: this.calcDeceptionScore(val)
        },
        { emitEvent: false }
      );
    });
  }

  calcDeceptionScore(formValues){
    return formValues.authoritative +
    formValues.grammar +
    formValues.internal + 
    formValues.link_domain +
    formValues.logo_graphics +
    formValues.public_news +
    formValues.relevancy_organization +
    formValues.sender_external
  }

  /**
   * Set the angular form data from the provided DeceptionCalculation model
   */
  setDeceptionFormFromModel(decep_calc_model: DeceptionCalculation) {
    
    this.deceptionFormGroup = new FormGroup({
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
      additional_word_tags: new FormControl(decep_calc_model.additional_word_tags, { updateOn: 'blur' }),
      final_deception_score: new FormControl({
        value: this.calcDeceptionScore(decep_calc_model), disabled:true}
      )
    });

  }

  setTemplatePreview(decep_model: DeceptionCalculation){
    this.templateName = decep_model.temlpateName ? decep_model.temlpateName : "Template name not found" 
    this.templateSubject = decep_model.templateSubject ? decep_model.templateSubject : "Template subject not found"
    this.templateHTML = decep_model.templateBody ? decep_model.templateBody : "<h1>Preivew not Found</h1>"
  }

  /**
   * Get the deception calculation model from the supplied form
   */
  getDeceptionModelFromForm(decep_form: FormGroup) {
    if (this.deceptionFormGroup.valid) {
      var decep_model = new DeceptionCalculation(this.deceptionFormGroup.value);
      var temp_model = new Template(<any>decep_model)
      console.log(temp_model)
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

    //this.router.navigate(['/templatemanager', this.templateId]);
  }

  setApperance(appearanceModel: any){
    
  }
  getAppearance(){

  }
}
