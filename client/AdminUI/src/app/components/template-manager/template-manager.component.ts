import {
  Component,
  OnInit,
  ViewChild,
  ElementRef,
  HostListener
} from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { AngularEditorConfig } from '@kolkov/angular-editor';
import { ActivatedRoute } from '@angular/router';
import { MyErrorStateMatcher } from 'src/app/helper/ErrorStateMatcher';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { TemplateManagerService } from 'src/app/services/template-manager.service';
import { Template } from 'src/app/models/template.model';
import { Subscription } from 'rxjs';
import $ from 'jquery';
import 'src/app/helper/csvToArray';

@Component({
  selector: 'app-template-manager',
  styleUrls: ['./template-manager.component.scss'],
  templateUrl: './template-manager.component.html'
})
export class TempalteManagerComponent implements OnInit {
  //Full template list variables
  template_list = [];
  search_input: string;

  //Body Form Variables
  templateId: string;
  currentTemplateFormGroup: FormGroup;
  matchSubject = new MyErrorStateMatcher();
  matchFromAddress = new MyErrorStateMatcher();
  matchTemplateName = new MyErrorStateMatcher();

  //Subscriptions
  subscriptions = Array<Subscription>();

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
    private route: ActivatedRoute
  ) {
    layoutSvc.setTitle('Template Manager');
    this.setEmptyTemplateForm();
    this.getAllTemplates();
  }
  ngOnInit() {
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
    this.subscriptions.push(
      this.route.params.subscribe(params => {
        this.templateId = params['templateId'];
        if (this.templateId != undefined) {
          this.selectTemplate(this.templateId);
        } else {
          this.setEmptyTemplateForm();
        }
      })
    );
  }

  ngOnDestroy() {
    this.subscriptions.forEach(sub => {
      sub.unsubscribe();
    });
  }

  ngAfterViewInit() {
    this.configAngularEditor();
  }

  getAllTemplates() {
    this.template_list = this.templateManagerSvc.getAllTemplates();
  }

  setEmptyTemplateForm() {
    this.currentTemplateFormGroup = new FormGroup({
      templateUUID: new FormControl(null),
      templateName: new FormControl('', [Validators.required]),
      templateDeceptionScore: new FormControl(0),
      templateDescriptiveWords: new FormControl(''),
      templateDescription: new FormControl(''),
      templateDisplayLink: new FormControl(''),
      templateFromAddress: new FormControl('', [Validators.required]),
      templateRetired: new FormControl(false),
      templateSubject: new FormControl('', [Validators.required]),
      templateText: new FormControl('', [Validators.required]),
      templateTopicList: new FormControl(''),
      templateGrammer: new FormControl(''),
      templateLinkDomain: new FormControl(''),
      templateLogoGraphics: new FormControl(''),
      templateExternal: new FormControl(''),
      templateInternal: new FormControl(''),
      templateAuthoratative: new FormControl(''),
      templateOrganization: new FormControl(''),
      templatePublicNews: new FormControl(''),
      templateFear: new FormControl(''),
      templateDutyObligation: new FormControl(''),
      templateCuriosity: new FormControl(''),
      templateGreed: new FormControl('')
    });
  }

  setTemplateForm(template: Template) {
    this.currentTemplateFormGroup = new FormGroup({
      templateUUID: new FormControl(template.template_uuid, [
        Validators.required
      ]),
      templateName: new FormControl(template.name, [Validators.required]),
      templateDeceptionScore: new FormControl(template.deception_score),
      templateDescriptiveWords: new FormControl(
        template.descriptive_words?.join(', ')
      ),
      templateDescription: new FormControl(template.description),
      templateDisplayLink: new FormControl(template.display_link),
      templateFromAddress: new FormControl(template.from_address, [
        Validators.required
      ]),
      templateRetired: new FormControl(template.retired),
      templateSubject: new FormControl(template.subject, [Validators.required]),
      templateText: new FormControl(template.text, [Validators.required]),
      templateTopicList: new FormControl(template.topic_list?.join(', ')),
      templateGrammer: new FormControl(template.grammer),
      templateLinkDomain: new FormControl(template.link_domain),
      templateLogoGraphics: new FormControl(template.logo_graphics),
      templateExternal: new FormControl(template.external),
      templateInternal: new FormControl(template.internal),
      templateAuthoratative: new FormControl(template.authoritative),
      templateOrganization: new FormControl(template.organization),
      templatePublicNews: new FormControl(template.public_news),
      templateFear: new FormControl(template.fear),
      templateDutyObligation: new FormControl(template.duty_obligation),
      templateCuriosity: new FormControl(template.curiosity),
      templateGreed: new FormControl(template.greed)
    });
  }

  getTemplateFromForm(form: FormGroup) {
    return new Template({
      template_uuid: form.controls['templateUUID'].value,
      name: form.controls['templateName'].value,
      deception_score: form.controls['templateDeceptionScore'].value,
      descriptive_words: form.controls[
        'templateDescriptiveWords'
      ].value?.csvToArray(),
      description: form.controls['templateDescription'].value,
      display_link: form.controls['templateDisplayLink'].value,
      from_address: form.controls['templateFromAddress'].value,
      retired: form.controls['templateRetired'].value,
      subject: form.controls['templateSubject'].value,
      text: form.controls['templateText'].value,
      topic_list: form.controls['templateTopicList'].value?.csvToArray(),
      grammer: form.controls['templateGrammer'].value,
      link_domain: form.controls['templateLinkDomain'].value,
      logo_graphics: form.controls['templateLogoGraphics'].value,
      external: form.controls['templateExternal'].value,
      internal: form.controls['templateInternal'].value,
      authoritative: form.controls['templateAuthoratative'].value,
      organization: form.controls['templateOrganization'].value,
      public_news: form.controls['templatePublicNews'].value,
      fear: form.controls['templateFear'].value,
      duty_obligation: form.controls['templateDutyObligation'].value,
      curiosity: form.controls['templateCuriosity'].value,
      greed: form.controls['templateGreed'].value
    });
  }

  newTemplate() {
    this.setEmptyTemplateForm();
  }
  selectTemplate(template_uuid: string) {
    if (this.currentTemplateFormGroup.dirty) {
      // alert(
      //   'Values not saved for ' +
      //     this.currentTemplateFormGroup.controls['templateName'].value
      // );
    }
    let selected_template = this.templateManagerSvc.getTemlpate(template_uuid);
    this.setTemplateForm(selected_template);
  }

  saveTemplate() {
    this.currentTemplateFormGroup.markAllAsTouched();
    if (this.currentTemplateFormGroup.valid) {
      let templateToSave = this.getTemplateFromForm(
        this.currentTemplateFormGroup
      );
      //Depending on API requirements, two methods are avaiable. One for put, one for post
      if (this.currentTemplateFormGroup.controls['templateUUID'].value == '0') {
        console.log('Attempting to create a new template');
        console.log(this.currentTemplateFormGroup);
        this.templateManagerSvc
          .saveTemplate(templateToSave)
          .then(val => console.log(val));
      } else {
        console.log(
          'updating template : ' +
            this.currentTemplateFormGroup.controls['templateUUID'].value
        );
        console.log(this.currentTemplateFormGroup);
        this.templateManagerSvc
          .saveTemplate(templateToSave)
          .then(val => console.log(val));
        //Update the new template with auto generated return variables (UUID, createddate,etc) to allow for navigation to deception calc
      }
    } else {
      const invalid = [];
      const controls = this.currentTemplateFormGroup.controls;
      for (const name in controls) {
        if (controls[name].invalid) {
          invalid.push(name);
        }
      }
      //TODO: replace with notification library when implmemnted
      alert('Invalid form fields: ' + invalid);
    }
  }

  onTabChanged($event) {
    //Required because the angular-editor library can not bind to [value].
    //Set the formGroups template text value to itself to force an update on tab switch
    this.currentTemplateFormGroup.controls['templateText'].setValue(
      this.currentTemplateFormGroup.controls['templateText'].value
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
    uploadUrl: 'TODO: REPLACE ME WITIH THE RIGHT URL',
    //uploadUrl: 'localhost:8080/server/page/upload-image',
    uploadWithCredentials: false,
    sanitize: true,
    toolbarPosition: 'top',
    toolbarHiddenButtons: [['bold', 'italic'], ['fontSize']]
  };
}
