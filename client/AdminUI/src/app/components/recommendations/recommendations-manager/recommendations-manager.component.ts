import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { AngularEditorConfig } from '@kolkov/angular-editor';
import { Router, ActivatedRoute } from '@angular/router';
import { MyErrorStateMatcher } from 'src/app/helper/ErrorStateMatcher';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { RecommendationsService } from 'src/app/services/recommendations.service';
import { Recommendations } from 'src/app/models/recommendations.model';
import $ from 'jquery';
import 'src/app/helper/csvToArray';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { AppSettings } from 'src/app/AppSettings';
import { ConfirmComponent } from '../../dialogs/confirm/confirm.component';
import { MatTableDataSource } from '@angular/material/table';
import { SettingsService } from 'src/app/services/settings.service';
import { AlertComponent } from '../../dialogs/alert/alert.component';

@Component({
    selector: 'app-recommendations-manager',
    styleUrls: ['./recommendations-manager.component.scss'],
    templateUrl: './recommendations-manager.component.html'
})
export class RecommendationsManagerComponent implements OnInit {
    dialogRefConfirm: MatDialogRef<ConfirmComponent>;

    //Full template list variables
    search_input: string;

    //Body Form Variables
    recommendationsId: string;
    retired: boolean;
    retiredReason: string;
    currentRecommendationsFormGroup: FormGroup;

    //config vars
    image_upload_url: string = `${this.settingsService.settings.apiUrl}/api/v1/imageupload/`;

    dateFormat = AppSettings.DATE_FORMAT;

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
        private recommendationsManagerSvc: RecommendationsService,
        private route: ActivatedRoute,
        private router: Router,
        private settingsService: SettingsService,
        public dialog: MatDialog
    ) {
        layoutSvc.setTitle('Recommendations Manager');
        //this.setEmptyTemplateForm();
        this.setRecommendationsForm(new Recommendations());
        //this.getAllTemplates();
    }

    ngOnInit() {
    }

    ngAfterViewInit() {
        this.configAngularEditor();
    }

    onValueChanges(): void {
        //Event fires for every modification to the form, used to update deception score
        this.currentRecommendationsFormGroup.valueChanges.subscribe(val => {
            this.currentRecommendationsFormGroup.patchValue(
                {
                    final_deception_score:
                        val.authoritative +
                        val.grammar +
                        val.internal +
                        val.link_domain +
                        val.logo_graphics +
                        val.public_news +
                        val.organization +
                        val.external
                },
                { emitEvent: false }
            );
        });
    }

    //Select a template based on template_uuid, returns the full template
    selectRecommendations(recommendations_uuid: string) {
        //Get template and call setRecommendationsForm to initialize a form group using the selected template
        this.recommendationsManagerSvc.getRecommendation(recommendations_uuid).then(
            success => {
                let t = <Recommendations>success;

                this.setRecommendationsForm(t);
                this.recommendationsId = t.recommendations_uuid;

            },
            error => { }
        );
    }

    //Create a formgroup using a Template as initial data
    setRecommendationsForm(recommendations: Recommendations) {
        if (!recommendations.appearance) {
            recommendations.appearance = <any>{};
        }
        if (!recommendations.sender) {
            recommendations.sender = <any>{};
        }
        if (!recommendations.relevancy) {
            recommendations.relevancy = <any>{};
        }
        if (!recommendations.behavior) {
            recommendations.behavior = <any>{};
        }

        this.currentRecommendationsFormGroup = new FormGroup({
            recommendationsUUID: new FormControl(recommendations.recommendations_uuid),
            recommendationsName: new FormControl(recommendations.name, [Validators.required]),
            recommendationsDescription: new FormControl(recommendations.description, [Validators.required]),
            recommendationsDeceptionScore: new FormControl(recommendations.deception_level),
            authoritative: new FormControl(recommendations.sender?.authoritative ?? 0),
            external: new FormControl(recommendations.sender?.external ?? 0),
            internal: new FormControl(recommendations.sender?.internal ?? 0),
            grammar: new FormControl(recommendations.appearance?.grammar ?? 0),
            link_domain: new FormControl(recommendations.appearance?.link_domain ?? 0),
            logo_graphics: new FormControl(recommendations.appearance?.logo_graphics ?? 0),
            organization: new FormControl(recommendations.relevancy.organization ?? 0),
            public_news: new FormControl(recommendations.relevancy.public_news ?? 0),
            fear: new FormControl(recommendations.behavior?.fear ?? false),
            duty_obligation: new FormControl(
                recommendations.behavior?.duty_obligation ?? false
            ),
            curiosity: new FormControl(recommendations.behavior?.curiosity ?? false),
            greed: new FormControl(recommendations.behavior?.greed ?? false),
        });

        this.onValueChanges();
    }

    calcDeceptionScore(formValues) {
        return (
            (formValues.sender?.authoritative ?? 0) +
            (formValues.sender?.external ?? 0) +
            (formValues.sender?.internal ?? 0) +
            (formValues.appearance?.grammar ?? 0) +
            (formValues.appearance?.link_domain ?? 0) +
            (formValues.appearance?.logo_graphics ?? 0) +
            (formValues.relevancy?.public_news ?? 0) +
            (formValues.relevancy?.organization ?? 0)
        );
    }

    //Get Template model from the form group
    getRecommendationsFromForm(form: FormGroup) {
        // form fields might not have the up-to-date content that the angular-editor has
        form.controls['recommendationsDescription'].setValue(
            this.angularEditorEle.textArea.nativeElement.description
        );
        let formRecommendations = new Recommendations(form.value);
        let saveRecommendations = new Recommendations({
            recommendations_uuid: form.controls['recommendationsUUID'].value,
            name: form.controls['recommendationsName'].value,
            description: form.controls['recommendationsDescription'].value,
        });
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
        saveRecommendations.deception_level = form.controls['deception_level'].value;
        return saveRecommendations;
    }

    /**
     *
     */
    onCancelClick() {
        this.router.navigate(['/recommendations']);
    }

    /**
     *
     */
    saveRecommendations() {
        // mark all as touched to ensure formgroup validation checks all fields on new entry
        this.currentRecommendationsFormGroup.markAllAsTouched();
        if (this.currentRecommendationsFormGroup.valid) {
            let recommendationsToSave = this.getRecommendationsFromForm(
                this.currentRecommendationsFormGroup
            );
            //PATCH - existing template update
            if (this.currentRecommendationsFormGroup.controls['recommendationsUUID'].value) {
                this.recommendationsManagerSvc.updateRecommendation(recommendationsToSave).then(
                    success => {
                        this.router.navigate(['/recommendations']);
                        // let retTemplate = <Template>success
                        // this.updateTemplateInList(retTemplate)
                    },
                    error => {
                        console.log(error);
                    }
                );
                //POST - new template creation
            } else {
                this.recommendationsManagerSvc.saveNewRecommendation(recommendationsToSave).then(
                    success => {
                        this.router.navigate(['/recommendations']);
                        // let retTemplate = new Template({
                        //   'template_uuid': success['template_uuid'],
                        //   '

                        // ': templateToSave.name,
                        //   'descriptive_words': templateToSave.descriptive_words,
                        //   'deception_score': 0
                        // })
                        // this.updateTemplateInList(retTemplate)
                    },
                    error => {
                        console.log(error);
                        if (error.status === 409) {
                            this.dialog.open(AlertComponent, {
                                // Parse error here
                                data: {
                                    title: 'Template Name Error',
                                    messageText: 'Template Name alreay exists.'
                                }
                            });
                        }
                    }
                );
            }
        } else {
            //non valid form, collect nonvalid fields and display to user
            const invalid = [];
            const controls = this.currentRecommendationsFormGroup.controls;
            for (const name in controls) {
                if (controls[name].invalid) {
                    invalid.push(name);
                }
            }
            this.dialog.open(AlertComponent, {
                data: {
                    title: 'Error',
                    messageText: 'Invalid form fields: ' + invalid
                }
            });
        }
    }

    deleteRecommendations() {
        let recommendations_to_delete = this.getRecommendationsFromForm(
            this.currentRecommendationsFormGroup
        );

        this.dialogRefConfirm = this.dialog.open(ConfirmComponent, {
            disableClose: false
        });
        this.dialogRefConfirm.componentInstance.confirmMessage = `Are you sure you want to delete ${recommendations_to_delete.name}?`;
        this.dialogRefConfirm.componentInstance.title = 'Confirm Delete';

        this.dialogRefConfirm.afterClosed().subscribe(result => {
            if (result) {
                this.recommendationsManagerSvc.deleteRecommendation(recommendations_to_delete).then(
                    success => {
                        this.router.navigate(['/recommendations']);
                    },
                    error => { }
                );
            }
            this.dialogRefConfirm = null;
        });
    }

    //Event that fires everytime the template tab choice is changed
    onTabChanged($event) {
        //Required because the angular-editor library can not bind to [value].
        //Set the formGroups template text value to itself to force an update on tab switch
        this.currentRecommendationsFormGroup.controls['recommendationsDescription'].setValue(
            this.currentRecommendationsFormGroup.controls['recommendationsDescription'].value
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

    // Config setting for the angular-editor
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
        placeholder: 'Please enter template text here...',
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
        toolbarHiddenButtons: [
            ['bold', 'italic'],
            ['fontSize', 'insertVideo']
        ]
    };
}