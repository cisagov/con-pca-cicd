import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChartsService {
  /**
   * Returns the data to draw the Statistics By Level charts.
   */
  getStatisticsByLevel() {
    return [
      {
        name: 'Sent',
        series: [
          {
            name: 'Low',
            value: 100
          },
          {
            name: 'Moderate',
            value: 125
          },
          {
            name: 'High',
            value: 106
          }
        ]
      },
      {
        name: 'Opened',
        series: [
          {
            name: 'Low',
            value: 81
          },
          {
            name: 'Moderate',
            value: 83
          },
          {
            name: 'High',
            value: 62
          }
        ]
      },
      {
        name: 'Clicked',
        series: [
          {
            name: 'Low',
            value: 50
          },
          {
            name: 'Moderate',
            value: 27
          },
          {
            name: 'High',
            value: 50
          }
        ]
      },
      {
        name: 'Submitted',
        series: [
          {
            name: 'Low',
            value: 10
          },
          {
            name: 'Moderate',
            value: 20
          },
          {
            name: 'High',
            value: 30
          }
        ]
      },
      {
        name: 'Reported',
        series: [
          {
            name: 'Low',
            value: 80
          },
          {
            name: 'Moderate',
            value: 50
          },
          {
            name: 'High',
            value: 20
          }
        ]
      }
    ];
  }

  /**
   * Returns the percentage of emails sent thus far in the cycle.
   */
  getSentEmailNumbers() {
    return [
      {
        name: '',
        series: [
          {
            name: 'Number Sent',
            value: 333
          },
          {
            name: 'Number Not Sent',
            value: 667
          }
        ]
      }
    ];
  }
}
