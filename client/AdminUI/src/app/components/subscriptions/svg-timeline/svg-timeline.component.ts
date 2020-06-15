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

  /**
   *
   */
  constructor() { }

  /**
   *
   */
  ngOnInit(): void {
    this.xyz();
  }

  /**
   *
   */
  xyz() {
    console.log('xyz');
    console.log(this.timelineItems);
    let itemIndex = 0;
    this.timelineItems.forEach(x => {
      const item = {
        x: itemIndex * 100
      };

      this.items.push(item);

      itemIndex = itemIndex + 1;
    });
  }

}
