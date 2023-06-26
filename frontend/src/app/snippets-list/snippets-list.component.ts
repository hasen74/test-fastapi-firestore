import { Component, OnInit } from '@angular/core';
import { SnippetService } from '../services/snippet.service';
import { Snippet } from 'src/snippets';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-snippets-list',
  templateUrl: './snippets-list.component.html',
  styleUrls: ['./snippets-list.component.css']
})
export class SnippetsListComponent implements OnInit {

  snippets: Snippet[] = [];

  constructor(
    private snippetService: SnippetService,
    private authService: AuthService
    ) {}

  user = JSON.stringify(this.authService.user);

  ngOnInit(): void {
    this.getSnippets();
  }

  getSnippets(): void {
    this.snippetService.getSnippets().subscribe((snippets: Snippet[]) => {
    this.snippets = snippets;
    console.log(this.snippets);
    console.log(this.authService.user)
    });
  }
}
