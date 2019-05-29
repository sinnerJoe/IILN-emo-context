import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule, routes } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { SubmitPageComponent } from './submit-page/submit-page.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatCardModule, MatButtonModule, MatInputModule, MatDividerModule, MatCard} from "@angular/material"
import { RouterModule } from '@angular/router';
@NgModule({
  declarations: [
    AppComponent,
    SubmitPageComponent
  ],
  imports: [
    MatCardModule,
    MatButtonModule,
    MatInputModule,
    BrowserAnimationsModule,
    BrowserModule,
    // AppRoutingModule,
    FormsModule,
    HttpClientModule,
    MatDividerModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
