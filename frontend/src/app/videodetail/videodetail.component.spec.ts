import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoDetailComponent } from './videodetail.component';

describe('VideodetailComponent', () => {
  let component: VideoDetailComponent;
  let fixture: ComponentFixture<VideoDetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [VideoDetailComponent]
    });
    fixture = TestBed.createComponent(VideoDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
