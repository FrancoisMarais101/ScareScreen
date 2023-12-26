import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoSearchComponent } from './videosearch.component';

describe('VideosearchComponent', () => {
  let component: VideoSearchComponent;
  let fixture: ComponentFixture<VideoSearchComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [VideoSearchComponent]
    });
    fixture = TestBed.createComponent(VideoSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
