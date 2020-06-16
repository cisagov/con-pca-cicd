import {
  Component,
  AfterViewInit,
  Input,
  Output,
  EventEmitter,
  ViewEncapsulation,
  OnInit,
  OnChanges,
  AfterContentInit
} from '@angular/core';
import { TimelineItem } from 'src/app/models/subscription.model';
import * as moment from 'node_modules/moment/moment';
import * as $ from 'jquery';

@Component({
  selector: 'timeline',
  styleUrls: ['./timeline.component.css'],
  templateUrl: './timeline.component.html',
  encapsulation: ViewEncapsulation.None
})
export class TimelineComponent implements OnChanges {
  @Input()
  timelineItems: TimelineItem[];
  @Input()
  selectedItemId: number = 0;

  selectedItemIdAfterInit: number = 0;

  @Output()
  timelineItemClicked = new EventEmitter<TimelineItem>();

  constructor() {}

  ngAfterViewInit(): void {}

  /**
   *
   */
  ngOnChanges(): void {
    var timelines = $('.cd-horizontal-timeline');

    if (timelines.length > 0 && this.timelineItems.length > 0) {
      if (this.selectedItemId == 0) {
        this.selectedItemId = this.timelineItems[
          this.timelineItems.length - 1
        ].id;
      }
      setTimeout(() => {
        initTimeline(timelines, this.timelineItems, this.selectedItemId);
      }, 300);
    }
  }

  /**
   *
   * @param item
   */
  timelineItemClick(item: TimelineItem) {
    this.timelineItemClicked.emit(item);
  }
}

function initTimeline(timelines, items, selectedId) {
  timelines.each(function() {
    var eventsMinDistance = $(this).data('spacing');
    eventsMinDistance = 40;
    var timeline = $(this);
    var timelineComponents = {};
    //cache timeline components
    timelineComponents['timelineWrapper'] = timeline.find('.events-wrapper');
    timelineComponents['eventsWrapper'] = timelineComponents[
      'timelineWrapper'
    ].children('.events');
    timelineComponents['fillingLine'] = timelineComponents[
      'eventsWrapper'
    ].children('.filling-line');
    timelineComponents['timelineEvents'] = timelineComponents[
      'eventsWrapper'
    ].find('a');
    timelineComponents['timelineDates'] = parseDate(items);
    timelineComponents['eventsMinLapse'] = minLapse(
      timelineComponents['timelineDates']
    );
    timelineComponents['timelineNavigation'] = timeline.find(
      '.cd-timeline-navigation'
    );
    timelineComponents['eventsContent'] = timeline.children('.events-content');

    //assign a left postion to the single events along the timeline
    setDatePosition(timelineComponents, eventsMinDistance);
    //assign a width to the timeline
    var timelineTotWidth = setTimelineWidth(
      timelineComponents,
      eventsMinDistance,
      selectedId
    );
    //the timeline has been initialize - show it
    timeline.addClass('loaded');

    //detect click on the next arrow
    timelineComponents['timelineNavigation'].on('click', '.next', function(
      event
    ) {
      event.preventDefault();
      updateSlide(
        timelineComponents,
        timelineTotWidth,
        'next',
        eventsMinDistance
      );
    });

    //detect click on the prev arrow
    timelineComponents['timelineNavigation'].on('click', '.prev', function(
      event
    ) {
      event.preventDefault();
      updateSlide(
        timelineComponents,
        timelineTotWidth,
        'prev',
        eventsMinDistance
      );
    });

    //detect click on the a single event - show new event content
    timelineComponents['eventsWrapper'].on('click', 'a', function(event) {
      event.preventDefault();
      timelineComponents['timelineEvents'].removeClass('selected');
      $(this).addClass('selected');
      this.selectedItemIdAfterInit = $(this).get(0).id;
      updateOlderEvents($(this));
      updateFilling(
        $(this),
        timelineComponents['fillingLine'],
        timelineTotWidth
      );
      updateVisibleContent($(this), timelineComponents['eventsContent']);
    });

    //on swipe, show next/prev event content
    timelineComponents['eventsContent'].on('swipeleft', function() {
      var mq = checkMQ();
      mq == 'mobile' &&
        showNewContent(timelineComponents, timelineTotWidth, 'next');
    });
    timelineComponents['eventsContent'].on('swiperight', function() {
      var mq = checkMQ();
      mq == 'mobile' &&
        showNewContent(timelineComponents, timelineTotWidth, 'prev');
    });

    //keyboard navigation
    $(document).keyup(function(event) {
      if (event.which == 37 && elementInViewport(timeline.get(0))) {
        showNewContent(timelineComponents, timelineTotWidth, 'prev');
      } else if (event.which == 39 && elementInViewport(timeline.get(0))) {
        showNewContent(timelineComponents, timelineTotWidth, 'next');
      }
    });
  });
}

function updateSlide(
  timelineComponents,
  timelineTotWidth,
  string,
  eventsMinDistance
) {
  //retrieve translateX value of timelineComponents['eventsWrapper']
  var translateValue = getTranslateValue(timelineComponents['eventsWrapper']),
    wrapperWidth = Number(
      timelineComponents['timelineWrapper'].css('width').replace('px', '')
    );
  //translate the timeline to the left('next')/right('prev')
  string == 'next'
    ? translateTimeline(
        timelineComponents,
        translateValue - wrapperWidth + eventsMinDistance,
        wrapperWidth - timelineTotWidth
      )
    : translateTimeline(
        timelineComponents,
        translateValue + wrapperWidth - eventsMinDistance,
        undefined
      );
}

function showNewContent(timelineComponents, timelineTotWidth, string) {
  //go from one event to the next/previous one
  var visibleContent = timelineComponents['eventsContent'].find('.selected'),
    newContent =
      string == 'next' ? visibleContent.next() : visibleContent.prev();

  if (newContent.length > 0) {
    //if there's a next/prev event - show it
    var selectedDate = timelineComponents['eventsWrapper'].find('.selected'),
      newEvent =
        string == 'next'
          ? selectedDate
              .parent('li')
              .next('li')
              .children('a')
          : selectedDate
              .parent('li')
              .prev('li')
              .children('a');

    updateFilling(
      newEvent,
      timelineComponents['fillingLine'],
      timelineTotWidth
    );
    updateVisibleContent(newEvent, timelineComponents['eventsContent']);
    newEvent.addClass('selected');
    selectedDate.removeClass('selected');
    updateOlderEvents(newEvent);
    updateTimelinePosition(string, newEvent, timelineComponents);
  }
}

function updateTimelinePosition(string, event, timelineComponents) {
  //translate timeline to the left/right according to the position of the selected event
  var eventStyle = window.getComputedStyle(event.get(0), null),
    eventLeft = Number(eventStyle.getPropertyValue('left').replace('px', '')),
    timelineWidth = Number(
      timelineComponents['timelineWrapper'].css('width').replace('px', '')
    ),
    timelineTotWidth = Number(
      timelineComponents['eventsWrapper'].css('width').replace('px', '')
    );
  var timelineTranslate = getTranslateValue(
    timelineComponents['eventsWrapper']
  );

  if (
    (string == 'next' && eventLeft > timelineWidth - timelineTranslate) ||
    (string == 'prev' && eventLeft < -timelineTranslate)
  ) {
    translateTimeline(
      timelineComponents,
      -eventLeft + timelineWidth / 2,
      timelineWidth - timelineTotWidth
    );
  }
}

function translateTimeline(timelineComponents, value, totWidth) {
  console.log('translateTimeline totWidth: ' + totWidth);
  var eventsWrapper = timelineComponents['eventsWrapper'].get(0);
  value = value > 0 ? 0 : value; //only negative translate value
  value =
    !(typeof totWidth === 'undefined') && value < totWidth ? totWidth : value; //do not translate more than timeline width
  setTransformValue(eventsWrapper, 'translateX', value + 'px');
  //update navigation arrows visibility
  value == 0
    ? timelineComponents['timelineNavigation']
        .find('.prev')
        .addClass('inactive')
    : timelineComponents['timelineNavigation']
        .find('.prev')
        .removeClass('inactive');
  value == totWidth
    ? timelineComponents['timelineNavigation']
        .find('.next')
        .addClass('inactive')
    : timelineComponents['timelineNavigation']
        .find('.next')
        .removeClass('inactive');
}

function updateFilling(selectedEvent, filling, totWidth) {
  //change .filling-line length according to the selected event
  console.log('updateFilling: totWidth: ' + totWidth);
  var eventStyle = window.getComputedStyle(selectedEvent.get(0), null),
    eventLeft = eventStyle.getPropertyValue('left'),
    eventWidth = eventStyle.getPropertyValue('width');

  eventLeft = (
    Number(eventLeft.replace('px', '')) +
    Number(eventWidth.replace('px', '')) / 2
  ).toString();
  var scaleValue = Number(eventLeft) / totWidth;
  setTransformValue(filling.get(0), 'scaleX', scaleValue);
}

function setDatePosition(timelineComponents, min) {
  for (var i = 0; i < timelineComponents['timelineDates'].length; i++) {
    var distanceMS = daydiff(
      timelineComponents['timelineDates'][0],
      timelineComponents['timelineDates'][i]
    );
    var distanceNorm =
      Math.round(distanceMS / timelineComponents['eventsMinLapse']) + 2;

    console.log(timelineComponents['timelineEvents'].eq(i));
    timelineComponents['timelineEvents']
      .eq(i)
      .css('left', distanceNorm * min + 'px');
  }
}

function setTimelineWidth(timelineComponents, width, selectedItemId) {
  console.log('setTimelineWidth: ' + width);
  console.log('timelineDates[0] = ' + timelineComponents['timelineDates'][0]);
  console.log(timelineComponents['timelineDates'][0]);
  var timeSpanMS = daydiff(
    timelineComponents['timelineDates'][0],
    timelineComponents['timelineDates'][
      timelineComponents['timelineDates'].length - 1
    ]
  );
  console.log('setTimelineWidth timeSpan = ' + timeSpanMS + ' ms');
  var timeSpanNorm = timeSpanMS / timelineComponents['eventsMinLapse'];
  console.log('timeSpanNorm: ' + timeSpanNorm);
  timeSpanNorm = Math.round(timeSpanNorm) + 4;
  var totalWidth = timeSpanNorm * width;

  // RKW
  //totalWidth = 800;

  timelineComponents['eventsWrapper'].css('width', totalWidth + 'px');

  updateFilling(
    timelineComponents['eventsWrapper'].find('a#' + selectedItemId),
    timelineComponents['fillingLine'],
    totalWidth
  );
  updateTimelinePosition(
    'next',
    timelineComponents['eventsWrapper'].find('a#' + selectedItemId),
    timelineComponents
  );
  return totalWidth;
}

function updateVisibleContent(event, eventsContent) {
  var eventId = event[0].id,
    visibleContent = eventsContent.find('.selected'),
    selectedContent = eventsContent.find('li#' + eventId),
    selectedContentHeight = selectedContent.height();

  if (selectedContent.index() > visibleContent.index()) {
    var classEntering = 'selected enter-right',
      classLeaving = 'leave-left';
  } else {
    var classEntering = 'selected enter-left',
      classLeaving = 'leave-right';
  }

  selectedContent.attr('class', classEntering);
  visibleContent
    .attr('class', classLeaving)
    .one(
      'webkitAnimationEnd oanimationend msAnimationEnd animationend',
      function() {
        visibleContent.removeClass('leave-right leave-left');
        selectedContent.removeClass('enter-left enter-right');
      }
    );
  eventsContent.css('height', selectedContentHeight + 'px');
}

function updateOlderEvents(event) {
  event
    .parent('li')
    .prevAll('li')
    .children('a')
    .addClass('older-event')
    .end()
    .end()
    .nextAll('li')
    .children('a')
    .removeClass('older-event');
}

function getTranslateValue(timeline) {
  var timelineStyle = window.getComputedStyle(timeline.get(0), null),
    timelineTranslate =
      timelineStyle.getPropertyValue('-webkit-transform') ||
      timelineStyle.getPropertyValue('-moz-transform') ||
      timelineStyle.getPropertyValue('-ms-transform') ||
      timelineStyle.getPropertyValue('-o-transform') ||
      timelineStyle.getPropertyValue('transform');

  if (timelineTranslate.indexOf('(') >= 0) {
    var timelineTranslate = timelineTranslate.split('(')[1];
    timelineTranslate = timelineTranslate.split(')')[0];
    var translateValue = timelineTranslate.split(',')[4];
  } else {
    var translateValue = '0';
  }

  return Number(translateValue);
}

function setTransformValue(element, property, value) {
  element.style['-webkit-transform'] = property + '(' + value + ')';
  element.style['-moz-transform'] = property + '(' + value + ')';
  element.style['-ms-transform'] = property + '(' + value + ')';
  element.style['-o-transform'] = property + '(' + value + ')';
  element.style['transform'] = property + '(' + value + ')';
}

//based on http://stackoverflow.com/questions/542938/how-do-i-get-the-number-of-days-between-two-dates-in-javascript
function parseDate(events) {
  var dateArrays = [];
  for (var i = 0; i < events.length; i++) {
    var dateComp = events[i].date.format('DD/MM/YYYY');
    var dayComp = dateComp.split('/');
    var timeComp = [0, 0];

    var newDate = new Date(
      dayComp[2],
      dayComp[1] - 1,
      dayComp[0],
      timeComp[0],
      timeComp[1]
    );
    dateArrays.push(newDate);
  }
  return dateArrays;
}

function daydiff(first, second) {
  return Math.round(second - first);
}

function minLapse(dates) {
  //determine the minimum distance among events
  var dateDistances = [];
  for (var i = 1; i < dates.length; i++) {
    var distance = daydiff(dates[i - 1], dates[i]);
    dateDistances.push(distance);
  }
  return Math.min.apply(null, dateDistances);
}

/*
    How to tell if a DOM element is visible in the current viewport?
    http://stackoverflow.com/questions/123999/how-to-tell-if-a-dom-element-is-visible-in-the-current-viewport
*/
function elementInViewport(el) {
  var top = el.offsetTop;
  var left = el.offsetLeft;
  var width = el.offsetWidth;
  var height = el.offsetHeight;

  while (el.offsetParent) {
    el = el.offsetParent;
    top += el.offsetTop;
    left += el.offsetLeft;
  }

  return (
    top < window.pageYOffset + window.innerHeight &&
    left < window.pageXOffset + window.innerWidth &&
    top + height > window.pageYOffset &&
    left + width > window.pageXOffset
  );
}

function checkMQ() {
  //check if mobile or desktop device
  return window
    .getComputedStyle(
      document.querySelector('.cd-horizontal-timeline'),
      '::before'
    )
    .getPropertyValue('content')
    .replace(/'/g, '')
    .replace(/"/g, '');
}
