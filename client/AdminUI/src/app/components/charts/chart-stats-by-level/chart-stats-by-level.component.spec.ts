import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartStatsByLevelComponent } from './chart-stats-by-level.component';

describe('ChartStatsByLevelComponent', () => {
  let component: ChartStatsByLevelComponent;
  let fixture: ComponentFixture<ChartStatsByLevelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChartStatsByLevelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChartStatsByLevelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
