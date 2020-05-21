import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-sending-profile-detail',
  templateUrl: './sending-profile-detail.component.html'
})
export class SendingProfileDetailComponent implements OnInit {

  profileForm: FormGroup;

  /**
   * 
   */
  constructor(
    public dialog_ref: MatDialogRef<SendingProfileDetailComponent>,
  ) { }

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
