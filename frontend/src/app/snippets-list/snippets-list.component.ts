import { Component, OnInit } from '@angular/core';
import { SnippetService } from '../services/snippet.service';
import { Snippet } from 'src/snippets';

@Component({
  selector: 'app-snippets-list',
  templateUrl: './snippets-list.component.html',
  styleUrls: ['./snippets-list.component.css']
})
export class SnippetsListComponent implements OnInit {

  snippets: Snippet[] = [];

  constructor(private snippetService: SnippetService) {}

  ngOnInit(): void {
    this.getSnippets();
  }

  getSnippets(): void {
    this.snippetService.getSnippets().subscribe((snippets: Snippet[]) => {
    this.snippets = snippets;
    console.log(this.snippets);
    });
  }
}
