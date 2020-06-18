import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SettingsService } from './settings.service';

@Injectable({
  providedIn: 'root'
})
export class ChartsService {

  /**
   * Constructor.
   */
  constructor(
    private http: HttpClient,
    private settingsService: SettingsService
  ) {
  }

  /**
   * Gets the subscriptions's statistics
   */
  getStatisticsReport(subscriptionUuid: string) {
    const url = `${this.settingsService.settings.apiUrl}/api/v1/reports/${subscriptionUuid}/`;
    return this.http.get(url);
  }

  /**
   * Converts the API response into an object that the chart can use.
   * 
   * NOTE!
   * This is temporary, until we can expand the API to return stats
   * partitioned by template deception level:  low, moderate, high.
   * For now, we will just create a series of single-bar graphs.
   */
  formatStatistics(reportResponse: any) {
    const chartObject = [
      {
        name: 'Sent',
          series: [
            {
              name: 'all levels',
              value: reportResponse.sent
            }
          ]
      },
      {
        name: 'Opened',
          series: [
            {
              name: 'all levels',
              value: reportResponse.opened
            }
          ]
      },
      {
        name: 'Clicked',
          series: [
            {
              name: 'all levels',
              value: reportResponse.clicked
            }
          ]
      }
    ];

    return chartObject;
  }

/**
 * This is a dummy function.  Don't use it.
 * Right now, its purpose is to illustrate the structure of
 * the data that needs to be returned in formatStatistics() above.
 * Once the real data is getting formatted like this, delete
 * this function.
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
getSentEmailNumbers(reportResponse: any) {
  return [
    {
      name: '',
      series: [
        {
          name: 'Number Sent',
          value: reportResponse.sent
        },
        {
          name: 'Number Not Sent',
          value: reportResponse.target_count - reportResponse.sent
        }
      ]
    }
  ];
}
}
