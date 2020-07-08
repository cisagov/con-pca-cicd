import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Recommendations } from 'src/app/models/recommendations.model';
import { SettingsService } from './settings.service';

const headers = {
    headers: new HttpHeaders().set('Content-Type', 'application/json'),
    params: new HttpParams()
};

@Injectable()
export class RecommendationsService {

    /**
     * Constructor.
     * @param http
     */
    constructor(
        private http: HttpClient,
        private settingsService: SettingsService
    ) { }

    /**
     * GET a list of all recommendations
     * @param retired
     */
    getAllRecommendations(retired: boolean = false) {
        let url = `${this.settingsService.settings.apiUrl}/api/v1/recommendations/`;
        if (retired) {
            url = `${url}?retired=true`;
        }
        return this.http.get(url, headers);
    }

    /**
     * GET a single recommendation using the provided recommendations_uuid
     * @param uuid
     */
    getRecommendation(uuid: string) {
        return new Promise((resolve, reject) => {
            this.http
                .get(`${this.settingsService.settings.apiUrl}/api/v1/recommendations/${uuid}`)
                .subscribe(
                    success => {
                        resolve(success);
                    },
                    error => {
                        reject(error);
                    },
                    () => { }
                );
        });
    }

    /**
     * POST a new recommendation
     * @param recommendation
     */
    saveNewRecommendation(recommendation: Recommendations) {
        return new Promise((resolve, reject) => {
            this.http
                .post(
                    `${this.settingsService.settings.apiUrl}/api/v1/recommendations/`,
                    recommendation
                )
                .subscribe(
                    success => {
                        resolve(success);
                    },
                    error => {
                        reject(error);
                    },
                    () => { }
                );
        });
    }

    /**
     * PATCH an existing recommendation with partial data
     * @param recommendation
     */
    updateRecommendation(recommendation: Recommendations) {
        return new Promise((resolve, reject) => {
            this.http
                .patch(
                    `${this.settingsService.settings.apiUrl}/api/v1/recommendations/${recommendation.recommendations_uuid}/`,
                    recommendation
                )
                .subscribe(
                    success => {
                        resolve(success);
                    },
                    error => {
                        reject(error);
                    },
                    () => { }
                );
        });
    }

    /**
     *
     * @param recommendation
     */
    deleteRecommendation(recommendation: Recommendations) {
        return new Promise((resolve, reject) => {
            this.http
                .delete(
                    `${this.settingsService.settings.apiUrl}/api/v1/recommendations/${recommendation.recommendations_uuid}/`
                )
                .subscribe(
                    success => {
                        resolve(success);
                    },
                    error => {
                        reject(error);
                    }
                );
        });
    }
}
