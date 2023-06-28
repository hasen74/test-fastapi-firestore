import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Snippet } from 'src/snippets';

@Injectable({
  providedIn: 'root'
})
export class SnippetService {

  constructor(private http: HttpClient) {  }

  private snippetsUrl = 'http://127.0.0.1:8000/snippets'

  getSnippets(): Observable<any> {
    return this.http.get<Snippet[]>(this.snippetsUrl);
  }
}
