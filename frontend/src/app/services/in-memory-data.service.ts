import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Video } from '../video';

@Injectable({
  providedIn: 'root',
})
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const videos = [
      { id: 12, name: 'Video 1', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description1', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" },
      { id: 13, name: 'Video 2', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description2', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" },
      { id: 14, name: 'Video 3', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description3', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" },
      { id: 15, name: 'Video 4', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description4', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" },
      { id: 16, name: 'Video 5', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description5', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" },
      { id: 17, name: 'Video 6', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description6', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" },
      { id: 18, name: 'Video 7', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description7', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" },
      { id: 19, name: 'Video 8', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description8', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" },
      { id: 20, name: 'Video 9', url: 'https://www.youtube.com/watch?v=iQXmlf3Sefg', description: 'This is a description9', tags: ['tag1', 'tag2', 'tag3'], likes: 0, dislikes: 0, comments: ['comment1', 'comment2', 'comment3'], thumbnail: "assets/images/images.jpg" }
    ];
    return {videos};
  }

  // Overrides the genId method to ensure that a video always has an id.
  // If the videos array is empty,
  // the method below returns the initial number (11).
  // if the videos array is not empty, the method below returns the highest
  // video id + 1.
  genId(videos: Video[]): number {
    return videos.length > 0 ? Math.max(...videos.map(video => video.id)) + 1 : 11;
  }
}
