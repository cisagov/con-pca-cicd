import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SendingProfileService {

  /**
   * Constructor.
   * @param http 
   */
  constructor(
    private http: HttpClient
  ) { }

  /**
   * Returns a promise with all sending profiles.
   */
  public getAllProfiles() {
    let url = `${environment.apiEndpoint}/api/v1/sendingprofiles/`;
    return this.http.get(url);
  }

  /**
   * 
   * @param profileId 
   */
  public getProfile(profileId: number) {
    let url = `${environment.apiEndpoint}/api/v1/sendingprofile/${profileId}/`
    return this.http.get(url);
  }
}
