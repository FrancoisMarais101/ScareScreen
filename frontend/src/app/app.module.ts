import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

// import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
// import { InMemoryDataService } from './services/in-memory-data.service';
import { MovieService } from './services/movie.service'; // Ensure this service is named correctly

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { VideoComponent } from './video/video.component';
import { VideoSearchComponent } from './videosearch/videosearch.component';
import { MessagesComponent } from './messages/messages.component';
import { VideoDetailComponent } from './videodetail/videodetail.component';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule
    // Remove the in-memory web api module to ensure HTTP requests go to your actual backend
  ],
  declarations: [
    AppComponent,
    DashboardComponent,
    VideoComponent,
    VideoSearchComponent,
    MessagesComponent,
    VideoDetailComponent
  ],
  providers: [
    MovieService // Make sure your service is listed in the providers array if it's not providedIn: 'root'
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
