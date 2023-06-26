import { HttpEvent, HttpHandler, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
 
import { AuthService } from './auth.service';
 
@Injectable({ 
  providedIn: 'root' 
}) 
export class InterceptorService { 
 
  constructor( 
    private authService: AuthService 
  ) { 
  } 
 
  intercept( 
    request: HttpRequest<any>, 
    next: HttpHandler 
  ): Observable<HttpEvent<any>> { 
    request = request.clone({ headers: request.headers.set('Content-type', 'application/json') }).clone({ 
      setHeaders: { 
        Authorization: `Bearer ${this.authService.getToken()}` 
      } 
    });     
 
    return next.handle(request) 
  }
}