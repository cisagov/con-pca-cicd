import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { LayoutMainService } from 'src/app/services/layout-main.service';
import { TemplateManagerService } from 'src/app/services/template-manager.service';
import { Recommendations } from 'src/app/models/recommendations.model';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: '',
  templateUrl: './recommendations.component.html',
  styleUrls: ['./recommendations.component.scss']
})
export class RecommendationsComponent implements OnInit, AfterViewInit {
  displayedColumns = ['name', 'deception_score', 'created_by'];
  recommendationsData = new MatTableDataSource<Recommendations>();
  search_input = '';
  @ViewChild(MatSort) sort: MatSort;

  showRetired: boolean = false;

  loading = true;

  constructor(
    private templateSvc: TemplateManagerService,
    private router: Router,
    private layoutSvc: LayoutMainService
  ) {
    layoutSvc.setTitle('Templates');
  }

  ngOnInit() {
    this.refresh();
  }

  refresh() {
    this.loading = true;
    this.templateSvc
      .getAllTemplates(this.showRetired)
      .subscribe((data: any) => {
        this.recommendationsData.data = data as Recommendations[];
        this.recommendationsData.sort = this.sort;
        this.loading = false;
      });
  }

  ngAfterViewInit(): void {
    this.recommendationsData.sort = this.sort;
  }

  public filterTemplates = (value: string) => {
    this.recommendationsData.filter = value.trim().toLocaleLowerCase();
  };
  public editRecommendations(recommendations: Recommendations) {
    this.router.navigate(['/recommendations', recommendations.recommendations_uuid]);
  }

  onRetiredToggle() {
    if (this.displayedColumns.includes('retired')) {
      this.displayedColumns.pop();
    } else {
      this.displayedColumns.push('retired');
    }
    this.refresh();
  }
}
