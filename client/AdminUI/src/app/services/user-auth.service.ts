import { Injectable } from '@angular/core';
import { Auth } from 'aws-amplify'
import { Subject, Observable, BehaviorSubject } from 'rxjs';
import { Router } from '@angular/router'
import { resolve } from 'dns';
import { rejects } from 'assert';

@Injectable({
  providedIn: 'root'
})
export class UserAuthService {

  currentAuthUser : any
  public currentAuthUserSubject: BehaviorSubject<any> = new BehaviorSubject<any>("Iniitial");
  

  constructor(
      private router: Router
  ) {
    this.currentAuthUserSubject.subscribe((value) => {
        this.currentAuthUser = value
    })
    this.userIsAuthenticated().then().catch(error => console.log(error))
  }

  //Handles amplify authentification notfications from Hub
  handleAuthNotification(data){
    //   if(data["channel"] === "auth"){
    //     if(data["payload"]["event"] === "signIn"){
    //     }
    //   }
  }

  signOut(){
      Auth.signOut()      
  }

  redirectToSignIn(){
      Auth.federatedSignIn()
  }

  //Check Authentication, refreshing if possible. Redirecting to sign in if not authenticated
  userIsAuthenticated(){
      return new Promise((resolve, reject) => {
        Auth.currentAuthenticatedUser()
            .then((success) => { 
                this.currentAuthUserSubject.next(success)
                resolve(true)
            })
            .catch((error) => { 
                reject(error)              
                this.redirectToSignIn()
            })
        })
  }

  getUserBehaviorSubject(): Observable<any> {
      return this.currentAuthUserSubject;
  }

  
  getUserTokens(){
    return new Promise((resolve, reject) => {
        Auth.currentAuthenticatedUser()
            .then((success) => { 
                this.currentAuthUserSubject.next(success)
                resolve({
                    idToken: success.signInUserSession.accessToken.jwtToken,
                    accessToken: success.signInUserSession.idToken.jwtToken
                  })
            })
            .catch((error) => { 
                reject(error)              
                this.redirectToSignIn()
            })
        })
  }


  getCurentAuthUser(){
    Auth.currentAuthenticatedUser().then(
        success => {
          return success
        },
        failed => {
          console.log("failed to get currently authenticated user")
          console.log(failed)
          return false
        }
    )   
  }

}
