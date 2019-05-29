import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SubmitPageComponent } from './submit-page/submit-page.component';

export const routes: Routes = [
  {
    path: "home",
    component: SubmitPageComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
