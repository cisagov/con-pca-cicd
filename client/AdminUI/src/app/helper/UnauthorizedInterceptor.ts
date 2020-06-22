import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { UserAuthService } from '../services/user-auth.service'

@Injectable()
export class UnauthorizedInterceptor implements HttpInterceptor {
    constructor(private userAuthSvc: UserAuthService) {}

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(request).pipe(catchError(err => {
            console.log("UNATHORIZED CHECK")
            if (err.status === 401) {
                console.log("UNATHORIZED !!!!")
                // auto logout if 401 response returned from api
                this.userAuthSvc.signOut()
                location.reload(true);
            }
            
            const error = err.error.message || err.statusText;
            return throwError(error);
        }))
    }
}