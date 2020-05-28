import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChartsService {

  sent: any = {};

  /**
   * 
   */
  public getGraphs() {
    return [{
      "name": "Sent",
      "series": [
        {
          "name": "Low",
          "value": 345
        },
        {
          "name": "Moderate",
          "value": 325
        },
        {
          "name": "High",
          "value": 325
        }
      ]
    },
    {
      "name": "Opened",
      "series": [
        {
          "name": "Low",
          "value": 300
        },
        {
          "name": "Moderate",
          "value": 300
        },
        {
          "name": "High",
          "value": 300
        }
      ]
    },
    {
      "name": "Clicked",
      "series": [
        {
          "name": "Low",
          "value": 50
        },
        {
          "name": "Moderate",
          "value": 100
        },
        {
          "name": "High",
          "value": 150
        }
      ]
    },
    {
      "name": "Subitted",
      "series": [
        {
          "name": "Low",
          "value": 10
        },
        {
          "name": "Moderate",
          "value": 20
        },
        {
          "name": "High",
          "value": 30
        }
      ]
    },
    {
      "name": "Reported",
      "series": [
        {
          "name": "Low",
          "value": 80
        },
        {
          "name": "Moderate",
          "value": 50
        },
        {
          "name": "High",
          "value": 20
        }
      ]
    }];

  }

  /**
   * Returns the percentage of emails sent thus far in the cycle.
   */
  getSentPercent() {
    return [{
      "name": "",
      "series": [
        {
          "name": "Number Sent",
          "value": 333
        },
        {
          "name": "Number Not Sent",
          "value": 667
        }
      ]
  }];
  }

}
