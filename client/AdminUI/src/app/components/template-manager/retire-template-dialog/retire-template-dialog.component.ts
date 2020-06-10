import { Component, OnInit, Inject } from '@angular/core';
import { TemplateManagerService } from 'src/app/services/template-manager.service';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Template } from 'src/app/models/template.model';

@Component({
  selector: 'app-retire-template-dialog',
  templateUrl: './retire-template-dialog.component.html',
  styleUrls: ['../template-manager.component.scss']
})
export class RetireTemplateDialogComponent implements OnInit {

  template: Template
  retiredDescription: string
  canRetire: boolean

  constructor(
    public dialogRef: MatDialogRef<RetireTemplateDialogComponent>,
    public templateSvc: TemplateManagerService,
    public dialog: MatDialog,
    @Inject(MAT_DIALOG_DATA) data: Template
  ) {
    this.template = data
  }

  ngOnInit(): void {
  }

  updateReason(): void {
    if (this.retiredDescription != '' && this.retiredDescription != null) {
      this.canRetire = true
    } else {
      this.canRetire = false
    }
  }

  retire(): void {
    this.template.retired = true
    this.template.retired_description = this.retiredDescription
    this.templateSvc.updateTemplate(this.template)
    this.dialogRef.close()
  }

  cancel(): void {
    this.dialogRef.close()
  }

  onNoClick(): void {
    this.dialogRef.close()
  }

}
