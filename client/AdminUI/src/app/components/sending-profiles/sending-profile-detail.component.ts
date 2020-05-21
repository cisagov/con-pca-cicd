import { Component, OnInit, Inject } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { SendingProfileService } from 'src/app/services/sending-profile.service';
import { SendingProfile } from 'src/app/models/sending-profile.model';

@Component({
  selector: 'app-sending-profile-detail',
  templateUrl: './sending-profile-detail.component.html'
})
export class SendingProfileDetailComponent implements OnInit {

  profileForm: FormGroup;
  sendingProfileId: number;
  profile: SendingProfile

  /**
   * Constructor.
   */
  constructor(
      private sendingProfileSvc: SendingProfileService,
      public dialog_ref: MatDialogRef<SendingProfileDetailComponent>,
      @Inject(MAT_DIALOG_DATA) public data: any
    ) {
      this.sendingProfileId = data.sendingProfileId;
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
      name: new FormControl(''),
      interfaceType: new FormControl(''),
      from: new FormControl(''),
      host: new FormControl(''),
      username: new FormControl(''),
      password: new FormControl('')
    });

    this.sendingProfileSvc.getProfile(this.sendingProfileId).subscribe((data: any) => {
      this.profile = data as SendingProfile;

      this.f.name.setValue(this.profile.name);
      this.f.interfaceType.setValue(this.profile.interface_type);
      this.f.from.setValue(this.profile.from_address);
      this.f.host.setValue(this.profile.host);
      this.f.username.setValue(this.profile.username);
      this.f.password.setValue(this.profile.password);
    },
    (err) => {
      console.log(err);
    });
  }

  /**
   * 
   */
  onSaveClick() {
    // save the thing

    this.dialog_ref.close();
  }

  /**
   * 
   */
  onCancelClick() {
    this.dialog_ref.close();
  }

}
