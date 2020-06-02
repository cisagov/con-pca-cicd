import {
  Component,
  OnInit,
  ViewChild,
  ElementRef,
} from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { AngularEditorConfig } from '@kolkov/angular-editor';
import { Router, ActivatedRoute } from '@angular/router';
import { MyErrorStateMatcher } from 'src/app/helper/ErrorStateMatcher';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { TemplateManagerService } from 'src/app/services/template-manager.service';
import { Template } from 'src/app/models/template.model';
import { Subscription } from 'rxjs';
import { environment } from 'src/environments/environment';
import $ from 'jquery';
import 'src/app/helper/csvToArray';
import { MatDialog } from '@angular/material/dialog';
import { StopTemplateDialogComponent } from './stop-template-dialog/stop-template-dialog.component';

@Component({
  selector: 'app-template-manager',
  styleUrls: ['./template-manager.component.scss'],
  templateUrl: './template-manager.component.html'
})
export class TemplateManagerComponent implements OnInit {
  //Full template list variables
  search_input: string;

  //Body Form Variables
  templateId: string;
  currentTemplateFormGroup: FormGroup;
  matchSubject = new MyErrorStateMatcher();
  matchFromAddress = new MyErrorStateMatcher();
  matchTemplateName = new MyErrorStateMatcher();
  matchTemplateHTML = new MyErrorStateMatcher();
  //Subscriptions
  subscriptions = Array<Subscription>();

  //config vars
  image_upload_url: string = `${environment.apiEndpoint}/api/v1/imageupload/`

  //Styling variables, required to properly size and display the angular-editor import
  body_content_height: number;
  text_editor_height: number;
  text_area_bot_marg: number = 20; //based on the default text area padding on a mat textarea element
  //Elements used to get reference sizes for styling
  @ViewChild('selectedTemplateTitle') titleElement: ElementRef;
  @ViewChild('tabs') tabElement: any;
  @ViewChild('angularEditor') angularEditorEle: any;

  constructor(
    private layoutSvc: LayoutMainService,
    private templateManagerSvc: TemplateManagerService,
    private route: ActivatedRoute,
    private router: Router,
    public dialog: MatDialog
  ) {
    layoutSvc.setTitle('Template Manager');
    //this.setEmptyTemplateForm();
    this.setTemplateForm(new Template)
    //this.getAllTemplates();
  }
  ngOnInit() {
    console.log(this.image_upload_url)
    //get subscription to height of page from main layout component
    this.subscriptions.push(
      this.layoutSvc.getContentHeightEmitter().subscribe(height => {
        this.body_content_height = height;
        if (this.titleElement != undefined) {
          this.setEditorHeight();
        }
      })
    );
    //get subscription to check for the sidenav element being set in layout, and close by default
    this.subscriptions.push(
      this.layoutSvc.getSideNavIsSet().subscribe(sideNavEmit => {
        this.layoutSvc.closeSideNav().then(() => {
          this.setEditorHeight();
        });
      })
    );
    //Check if template ID was included in the route, open template identified if so
    this.subscriptions.push(
      this.route.params.subscribe(params => {
        this.templateId = params['templateId'];
        if (this.templateId != undefined) {
          this.selectTemplate(this.templateId);
        } else {
          //Use preset empty form
        }
      })
    );

  }

  
  ngOnDestroy() {
    //Unsubscribe from all subscriptions
    this.subscriptions.forEach(sub => {
      sub.unsubscribe();
    });
  }

  ngAfterViewInit() {
    this.configAngularEditor();
  }

  onValueChanges(): void {
    //Event fires for every modification to the form, used to update deception score
    this.currentTemplateFormGroup.valueChanges.subscribe(val => {
      this.currentTemplateFormGroup.patchValue(
        {
          final_deception_score:  (
            val.authoritative +
            val.grammar +
            val.internal + 
            val.link_domain +
            val.logo_graphics +
            val.public_news +
            val.organization +
            val.external
          )
        },
        { emitEvent: false }
      );
    });
  }

  //Select a template based on template_uuid, returns the full template
  selectTemplate(template_uuid: string) {
    //Get template and call setTemplateForm to initialize a form group using the selected template
    this.templateManagerSvc
      .getTemplate(template_uuid).then(
        (success) => {
          this.setTemplateForm(<Template>success)
          this.templateId = success['template_uuid']
        },
        (error) => {          
        }
      )
  }

  //Create a formgroup using a Template as initial data
  setTemplateForm(template: Template) {

    if(!template.appearance){template.appearance = <any>{}}
    if(!template.sender){template.sender = <any>{}}
    if(!template.relevancy){template.relevancy = <any>{}}
    if(!template.behavior){template.behavior = <any>{}}


    this.currentTemplateFormGroup = new FormGroup({
      templateUUID: new FormControl(template.template_uuid),
      templateName: new FormControl(template.name, [Validators.required]),
      templateDeceptionScore: new FormControl(template.deception_score),
      templateDescriptiveWords: new FormControl(template.descriptive_words),
      templateDescription: new FormControl(template.description),
      templateFromAddress: new FormControl(template.from_address, [
        Validators.required
      ]),
      templateRetired: new FormControl(template.retired),
      templateRetiredDescription: new FormControl(template.retired_description),
      templateSubject: new FormControl(template.subject, [Validators.required]),
      templateText: new FormControl(template.text),
      templateHTML: new FormControl(template.html, [Validators.required]),
      authoritative: new FormControl(template.sender?.authoritative ?? 0),
      external: new FormControl(template.sender?.external ?? 0),
      internal: new FormControl(template.sender?.internal ?? 0),      
      grammar: new FormControl(template.appearance?.grammar ?? 0),
      link_domain: new FormControl(template.appearance?.link_domain ?? 0),
      logo_graphics: new FormControl(template.appearance?.logo_graphics ?? 0),
      organization: new FormControl(template.relevancy.organization ?? 0),
      public_news: new FormControl(template.relevancy.public_news ?? 0),
      fear: new FormControl(template.behavior?.fear ?? false),
      duty_obligation: new FormControl(template.behavior?.duty_obligation ?? false),
      curiosity: new FormControl(template.behavior?.curiosity ?? false),
      greed: new FormControl(template.behavior?.greed ?? false),
      descriptive_words: new FormControl(template.descriptive_words ?? " ", { updateOn: 'blur' }),
      final_deception_score: new FormControl({
        value: this.calcDeceptionScore(template), disabled:true}
      )
    });
    
    this.onValueChanges();
  }
  
  calcDeceptionScore(formValues){
      return (formValues.sender?.authoritative ?? 0) +
      (formValues.sender?.external ?? 0) +
      (formValues.sender?.internal ?? 0) + 
      (formValues.appearance?.grammar ?? 0) +
      (formValues.appearance?.link_domain ?? 0) +
      (formValues.appearance?.logo_graphics ?? 0) +
      (formValues.relevancy?.public_news ?? 0) +
      (formValues.relevancy?.organization ?? 0)
  }

  //Get Template model from the form group
  getTemplateFromForm(form: FormGroup) {
      let formTemplate = new Template(form.value)
      let saveTemplate = new Template({
        template_uuid: form.controls['templateUUID'].value,
        name: form.controls['templateName'].value,
        deception_score: form.controls['templateDeceptionScore'].value,
        descriptive_words: form.controls['templateDescriptiveWords'].value,
        description: form.controls['templateDescription'].value,
        from_address: form.controls['templateFromAddress'].value,
        retired: form.controls['templateRetired'].value,
        retired_description: form.controls['templateRetiredDescription'].value,
        subject: form.controls['templateSubject'].value,
        text: form.controls['templateText'].value,
        html: form.controls['templateHTML'].value,
      })
      saveTemplate.appearance = { 
        'grammar': formTemplate.grammar,
        'link_domain': formTemplate.link_domain,
        'logo_graphics': formTemplate.logo_graphics
      }
      saveTemplate.sender = {
        'authoritative': formTemplate.authoritative,
        'external': formTemplate.external,
        'internal': formTemplate.internal
      }
      saveTemplate.relevancy = {
        'organization': formTemplate.organization,
        'public_news': formTemplate.public_news
      }
      saveTemplate.behavior = {
        'curiosity': formTemplate.curiosity,
        'duty_obligation': formTemplate.duty_obligation,
        'fear': formTemplate.fear,
        'greed': formTemplate.greed
      }
      saveTemplate.template_uuid = this.templateId
      saveTemplate.deception_score = form.controls['final_deception_score'].value
      return saveTemplate;
  }

  saveTemplate() {
    //mark all as touched to ensure formgroup validation checks all fields on new entry
    this.currentTemplateFormGroup.markAllAsTouched();
    if (this.currentTemplateFormGroup.valid) {
      let templateToSave = this.getTemplateFromForm(
        this.currentTemplateFormGroup
      );
      //PATCH - existing template update
      if (this.currentTemplateFormGroup.controls['templateUUID'].value) {
        this.templateManagerSvc
          .updateTemplate(templateToSave)
          .then(
            (success) => {
              this.router.navigate(['/templates']);
              // let retTemplate = <Template>success
              // this.updateTemplateInList(retTemplate)
            },
            (error) => {console.log(error)}
            );
      //POST - new template creation
      } else {
        this.templateManagerSvc
          .saveNewTemplate(templateToSave).then(
          (success) => {
            this.router.navigate(['/templates']);
            // let retTemplate = new Template({
            //   'template_uuid': success['template_uuid'],
            //   'name': templateToSave.name,
            //   'descriptive_words': templateToSave.descriptive_words,
            //   'deception_score': 0
            // })
            // this.updateTemplateInList(retTemplate)
          },
          (error) => {console.log(error)}
          );
      }
      
    } else {
    //non valid form, collect nonvalid fields and display to user
      const invalid = [];
      const controls = this.currentTemplateFormGroup.controls;
      for (const name in controls) {
        if (controls[name].invalid) {
          invalid.push(name);
        }
      }
      alert('Invalid form fields: ' + invalid);
    }
  }

  deleteTemplate(){
    let template_to_delete = this.getTemplateFromForm(this.currentTemplateFormGroup)  
    if(window.confirm(`Are you sure you want to delete ${template_to_delete.name}?`)){
    this.templateManagerSvc.deleteTemplate(template_to_delete)
      .then(
        (success) => {
          // this.updateTemplateInList(<Template>success)
          // this.setEmptyTemplateForm()
          this.router.navigate(['/templatespage']);
        },
        (error) => {}
      )
    }
  }

  openStopTemplateDialog() {
    let template_to_stop = this.getTemplateFromForm(this.currentTemplateFormGroup)

    this.dialog.open(
      StopTemplateDialogComponent, {
        data: template_to_stop
      }
    )
  }

  //Event that fires everytime the template tab choice is changed
  onTabChanged($event) {
    //Required because the angular-editor library can not bind to [value].
    //Set the formGroups template text value to itself to force an update on tab switch
    this.currentTemplateFormGroup.controls['templateHTML'].setValue(
      this.currentTemplateFormGroup.controls['templateHTML'].value
    );
  }
  

  //Required because the angular-editor requires a hard coded height. Sets a new height referencing the elements on the page for
  //an accurate hieght measurement
  setEditorHeight() {
    //height of the selected Template input and deceptioncalculator button div
    let selected_template_height = this.titleElement.nativeElement.offsetHeight;
    //height of the tabs
    let tab_height = this.tabElement._tabHeader._elementRef.nativeElement
      .clientHeight;
    //height of the space created between teh text area and the bottom of the tab structure
    let mat_text_area_height = $('.mat-form-field-infix')[0].clientHeight;
    //
    let save_button_row_height = 54;
    //Calculate the height allocated for the text areas, the text-area will use this directly while the editor will require assingment
    this.text_editor_height =
      this.body_content_height -
      selected_template_height -
      tab_height -
      mat_text_area_height -
      save_button_row_height;

    //Get the angular-editor toolbar height as it changes when the buttons wrap
    let angular_editor_tool_bar_height = $('.angular-editor-toolbar')[0]
      .clientHeight;
    //Set the editorConfig height to the text area height minus the toolbar height
    this.editorConfig['height'] =
      this.text_editor_height - angular_editor_tool_bar_height + 'px';
    this.editorConfig['maxHeight'] =
      this.text_editor_height - angular_editor_tool_bar_height + 'px';
    this.editorConfig['minHeight'] =
      this.text_editor_height - angular_editor_tool_bar_height + 'px';
    //remove the height from the text-area height to allow for the margin addition
    //Required to prevent the angular mat text area from overflowing onto its own border
    this.text_editor_height -= this.text_area_bot_marg;
  }

  //Configure elemenets of the angular-editor that are not included in the libraries config settings
  configAngularEditor() {
    let text_area = $('.angular-editor-textarea').first();
    text_area.css('resize', 'none');
    text_area.css('margin-bottom', '22px');
  }

  //Config setting for the angular-editor
  editorConfig: AngularEditorConfig = {
    editable: true,
    spellcheck: true,
    height: '500px',
    minHeight: '0',
    maxHeight: 'auto',
    width: 'auto',
    minWidth: '0',
    translate: 'yes',
    enableToolbar: true,
    showToolbar: true,
    placeholder:
      'Select a template on the left to edit or start typing to create a new template...',
    defaultParagraphSeparator: '',
    defaultFontName: '',
    defaultFontSize: '',
    fonts: [
      { class: 'arial', name: 'Arial' },
      { class: 'times-new-roman', name: 'Times New Roman' },
      { class: 'calibri', name: 'Calibri' },
      { class: 'comic-sans-ms', name: 'Comic Sans MS' }
    ],
    customClasses: [
      {
        name: 'quote',
        class: 'quote'
      },
      {
        name: 'redText',
        class: 'redText'
      },
      {
        name: 'titleText',
        class: 'titleText',
        tag: 'h1'
      }
    ],
    uploadUrl: this.image_upload_url,
    //uploadUrl: 'localhost:8080/server/page/upload-image',
    uploadWithCredentials: false,
    sanitize: true,
    toolbarPosition: 'top',
    toolbarHiddenButtons: [['bold', 'italic'], ['fontSize', 'insertVideo']]
  };
}
