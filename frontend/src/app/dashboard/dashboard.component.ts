import { Component, OnInit } from '@angular/core';
import { Video } from '../video'; // updated import
import { VideoService } from '../services/video.service';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
  videos: Video[] = []; // changed heroes to videos

  constructor(private videoService: VideoService) { } // updated constructor

  ngOnInit(): void {
    this.getVideos(); // renamed method
  }

  getVideos(): void { // renamed method
    this.videoService.getVideos() // changed getHeroes to getVideos
      .subscribe(videos => this.videos = videos.slice(1, 5)); // changed heroes to videos
  }
}
