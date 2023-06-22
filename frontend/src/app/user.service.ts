import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(
    private http: HttpClient
  ) { }

  private authUrl = 'http://127.0.0.1:8000/users/auth'

  authUser(token: string): Observable<any> {
    const url = `${this.authUrl}/${token}`;
  
    return this.http.get<string>(url);
  }
}
