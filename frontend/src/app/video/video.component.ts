import { Component, OnInit } from '@angular/core';

import { Video } from '../video'; // updated import
import { VideoService } from '../services/video.service';


@Component({
  selector: 'app-videos',
  templateUrl: './video.component.html', // updated templateUrl
  styleUrls: ['./video.component.css'] // updated styleUrls
})
export class VideoComponent implements OnInit { // renamed class to VideoComponent
  videos: Video[] = []; // changed heroes to videos

  constructor(private videoService: VideoService) { } // updated constructor

  ngOnInit(): void {
    this.getVideos(); // renamed method
  }

  getVideos(): void { // renamed method
    this.videoService.getVideos() // changed getHeroes to getVideos
    .subscribe(videos => this.videos = videos); // changed heroes to videos
  }

  add(name: string): void {
    name = name.trim();
    if (!name) { return; }
    this.videoService.addVideo({ name } as Video) // changed addHero to addVideo
      .subscribe(video => { // changed hero to video
        this.videos.push(video); // changed heroes to videos
      });
  }

  delete(video: Video): void { // changed hero to video
    this.videos = this.videos.filter(v => v !== video); // changed heroes to videos
    this.videoService.deleteVideo(video.id).subscribe(); // changed deleteHero to deleteVideo
  }
}
