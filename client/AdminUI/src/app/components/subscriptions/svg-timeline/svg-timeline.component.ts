import { Component, OnInit, Input } from '@angular/core';
import { TimelineItem } from 'src/app/models/subscription.model';

@Component({
  selector: 'app-svg-timeline',
  templateUrl: './svg-timeline.component.html'
})
export class SvgTimelineComponent implements OnInit {

  @Input()
  timelineItems: TimelineItem[];

  items: any[] = [];

  totalWidth = 1000;

  iconLaunch = '&#xf135;';
  iconCalendar = '&#xf073';
  iconToday = '&#xf274;';

  /**
   *
   */
  constructor() { }

  /**
   *
   */
  ngOnInit(): void {
    setTimeout(() => {
      this.drawTimeline();
    }, 300);
  }

  /**
   *
   */
  drawTimeline() {
    let itemX = 100;
    this.timelineItems.forEach(x => {
      const item = {
        x: itemX,
        date: x.date,
        title: x.title,
        icon: this.iconCalendar
      };

      if (item.title.toLowerCase() === 'subscription started') {
        item.icon = this.iconLaunch;
      }

      if (item.title.toLowerCase() === 'today') {
        item.icon = this.iconToday;
      }

      this.items.push(item);

      itemX += 200;
    });
  }

}
