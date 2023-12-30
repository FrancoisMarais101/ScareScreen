export interface Movie {
  age_restriction: number;
  cast: string;
  director: string;
  id: number;
  length: number; // assuming this is in minutes
  rating: number; // assuming this is the average rating
  release_date: string; // or Date if you wish to convert the string to a Date object
  summary: string;
  title: string;
}
