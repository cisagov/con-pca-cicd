import { Component, OnInit, Inject, ChangeDetectorRef, AfterViewChecked, AfterViewInit, AfterContentInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { SendingProfileService } from 'src/app/services/sending-profile.service';
import { SendingProfile, SendingProfileHeader } from 'src/app/models/sending-profile.model';

@Component({
  selector: 'app-sending-profile-detail',
  templateUrl: './sending-profile-detail.component.html'
})
export class SendingProfileDetailComponent implements OnInit, AfterContentInit {

  /** 
   * NEW or EDIT
   */
  mode: string = 'new';

  profileForm: FormGroup;
  id: number;
  profile: SendingProfile

  submitted = false;

  headers: Map<string, string> = new Map<string, string>();


  /**
   * Constructor.
   */
  constructor(
    private sendingProfileSvc: SendingProfileService,
    private changeDetector: ChangeDetectorRef,
    public dialog_ref: MatDialogRef<SendingProfileDetailComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.id = data.sendingProfileId;
  }

  /**
   * convenience getter for easy access to form fields
   */
  get f() { return this.profileForm.controls; }

  /**
   * 
   */
  ngOnInit(): void {
    this.profileForm = new FormGroup({
      name: new FormControl('', Validators.required),
      interfaceType: new FormControl(''),
      from: new FormControl('', [Validators.required, Validators.email]),
      host: new FormControl('', Validators.required),
      username: new FormControl(''),
      password: new FormControl(''),
      ignoreCertErrors: new FormControl(false),
      newHeaderName: new FormControl(''),
      newHeaderValue: new FormControl('')
    });

    if (!!this.id) {
      this.mode = 'edit';

      this.sendingProfileSvc.getProfile(this.id).subscribe((data: any) => {
        this.profile = data as SendingProfile;

        this.f.name.setValue(this.profile.name);
        this.f.interfaceType.setValue(this.profile.interface_type);
        this.f.from.setValue(this.profile.from_address);
        this.f.host.setValue(this.profile.host);
        this.f.username.setValue(this.profile.username);
        this.f.password.setValue(this.profile.password);
        this.f.ignoreCertErrors.setValue(this.profile.ignore_cert_errors);
        for (let h of this.profile.headers) {
          this.headers.set(h.key, h.value);
        }
      },
        (err) => {
          console.log(err);
        });
    }

    this.changeDetector.detectChanges();
  }

  /**
   * 
   */
  ngAfterContentInit(): void {
    this.changeDetector.detectChanges();
  }

  /**
   * Adds a custom email header to the internal list.
   */
  addHeader() {
    let key = this.f.newHeaderName.value.trim();
    if (key == "") {
      return;
    }
    this.headers.set(key, this.f.newHeaderValue.value.trim());
    this.f.newHeaderName.setValue("");
    this.f.newHeaderValue.setValue("");
    this.changeDetector.detectChanges();
  }

  /**
   * Deletes a custom email header from the internal list.
   */
  deleteHeader(headerKey: any) {
    this.headers.delete(headerKey);
    this.changeDetector.detectChanges();
  }

  /**
   * 
   */
  onSaveClick() {
    this.submitted = true;

    if (this.profileForm.invalid) {
      return;
    }

    let sp = new SendingProfile();
    sp.name = this.f.name.value;
    sp.username = this.f.username.value;
    sp.password = this.f.password.value;
    sp.host = this.f.host.value;
    sp.interface_type = this.f.interfaceType.value;
    sp.from_address = this.f.from.value;
    sp.ignore_cert_errors = this.f.ignoreCertErrors.value;
    sp.headers = [];
    for (let [key, value] of this.headers) {
      let h = {
        "key": key,
        "value": value
      };
      sp.headers.push(h);
    };
    
    if (this.id) {
      sp.id = this.id;
    }

    this.sendingProfileSvc.saveProfile(sp).subscribe(() => {
      this.dialog_ref.close();
    });
  }

  /**
   * 
   */
  onCancelClick() {
    this.dialog_ref.close();
  }
}
