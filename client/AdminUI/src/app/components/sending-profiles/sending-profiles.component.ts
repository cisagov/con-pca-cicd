import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { SendingProfile } from 'src/app/models/sending-profile.model';
import { SendingProfileService } from 'src/app/services/sending-profile.service';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { SendingProfileDetailComponent } from './sending-profile-detail.component';

@Component({
  selector: 'app-sending-profiles',
  templateUrl: './sending-profiles.component.html'
})
export class SendingProfilesComponent implements OnInit {

  displayedColumns = [
    "name",
    "interface_type",
    "modified_date"
  ];
  sendingProfilesData = new MatTableDataSource<SendingProfile>();

  constructor(
    private sendingProfileSvc: SendingProfileService,
    public dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.sendingProfileSvc.getAllProfiles().subscribe((data: any) => {
      this.sendingProfilesData.data = data as SendingProfile[];
    });
  }
  /**
   * 
   * @param row 
   */
  editProfile(row: any): void {
    // opens the same dialog in edit mode
  }

  /**
   * Open the detail dialog and pass the ID of the clicked row, or 0 if they clicked 'new'.
   */
  openProfileDialog(row: any): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.width = "60vw";
    dialogConfig.data = {
      sendingProfileId: row.id
    };
    const dialogRef = this.dialog.open(SendingProfileDetailComponent, dialogConfig);

    dialogRef.afterClosed().subscribe(value => {
      //
    })
  }
}
