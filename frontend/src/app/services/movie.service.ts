import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Movie } from '../models/movie'; // This should be the model representing your data structure

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private moviesUrl = 'http://localhost:8000/api/movies'; // URL to web api

  constructor(private http: HttpClient) { }

  getMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>(this.moviesUrl);
  }
}
