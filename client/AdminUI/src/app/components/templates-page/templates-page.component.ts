import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router'
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { TemplateManagerService } from 'src/app/services/template-manager.service';
import { Template } from 'src/app/models/template.model';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: '',
  templateUrl: './templates-page.component.html',
  styleUrls: ['./templates-page.component.scss']
})

export class TemplatesPageComponent implements OnInit, AfterViewInit{

  displayedColumns = [
    "name",
    "deception_score",
    "template_type",
    "created_by",
    "retired"
   ];
   templatesData = new MatTableDataSource<Template>();
   search_input = ''
   @ViewChild(MatSort) sort: MatSort

  constructor(
    private templateSvc: TemplateManagerService,
    private router: Router,
    private layoutSvc: LayoutMainService,
    ) {
      layoutSvc.setTitle("Templates");
   }

  ngOnInit() {
    this.templateSvc.getAllTemplates().subscribe((data: any) => {
      this.templatesData.data = data as Template[]
    })
  }

  ngAfterViewInit() : void {
    this.templatesData.sort = this.sort
  }

  public filterTemplates = (value: string) => {
    this.templatesData.filter = value.trim().toLocaleLowerCase();
  }
  public editTemplate(template: Template){
    this.router.navigate(['/templatemanager', template.template_uuid]);
  }
}