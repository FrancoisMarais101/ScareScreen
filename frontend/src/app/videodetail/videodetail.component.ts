import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Video } from '../video'; // updated import
import { VideoService } from '../services/video.service';

@Component({
  selector: 'app-videodetail',
  templateUrl: './videodetail.component.html',
  styleUrls: ['./videodetail.component.css']
})
export class VideoDetailComponent implements OnInit {
  video: Video | undefined;

  constructor(
    private route: ActivatedRoute,
    private videoService: VideoService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getVideo();
  }

  getVideo(): void {
    const id = parseInt(this.route.snapshot.paramMap.get('id')!, 10);
    this.videoService.getVideo(id)
      .subscribe(video => this.video = video);
  }

  goBack(): void {
    this.location.back();
  }

  save(): void {
    if (this.video) {
      this.videoService.updateVideo(this.video)
        .subscribe(() => this.goBack());
    }
  }
}