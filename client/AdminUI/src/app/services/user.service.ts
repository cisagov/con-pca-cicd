import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor() {}

  /**
   * Returns the current logged-in user
   */
  getCurrentUser() {
    return 'TEST USER';
  }
}
