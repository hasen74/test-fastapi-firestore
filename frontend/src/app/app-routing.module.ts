import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SnippetsListComponent } from './snippets-list/snippets-list.component';
import { AppComponent } from './app.component';

const routes: Routes = [
  { path: 'snippets', component: SnippetsListComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
