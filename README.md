# ScareScreen Guide

## Project Overview
ScareScreen is a comprehensive horror movie guide combining various technologies including Python, PostgreSQL, and several APIs. Our project is centered around horror movies and aims to provide a rich and detailed database for enthusiasts of the genre.

## Features

### Horror Movie Database
We use Python to scrape data from various online resources and create a comprehensive horror movie database in PostgreSQL. The data includes movie title, director, cast, release date, movie length, rating, age restriction, and a brief summary.

### Trailer Aggregator
We integrate APIs from platforms like YouTube to fetch trailers for each movie in our database. Whenever a user looks up a movie, the application also provides the trailer for a complete overview.

### Streaming Platform Finder
For each movie, we find out which online streaming platforms have the movie available (Netflix, Amazon Prime, Hulu, etc.). There are APIs available which help us fetch this information. We also scrape this data from various sources and keep it updated in our database.

### User Reviews and Ratings
We allow users to register and log in to leave their own ratings and reviews for each movie. We use Python’s Flask for the web backend, and PostgreSQL for storing user data and reviews.

### Recommendation Engine
Based on a user's past reviews and ratings, we've implemented a recommendation engine that suggests horror movies they might like. We've used Python's scikit-learn library to develop this recommendation system. Possibly using LightGBM

### Automation & Notifications
We've implemented a feature to notify users about new additions to the database, or when a movie from their watchlist becomes available on a streaming platform. We use Celery to manage these periodic tasks, and RabbitMQ as the message broker.

### Testing and CI/CD
We use Pytest for testing the Python components, and GitHub Actions for the CI/CD pipeline.

## Why ScareScreen?
This project provides a fantastic opportunity to delve deeper into Python and PostgreSQL, combining various technologies to deliver a comprehensive solution. And best of all, it centers around a topic we love - horror movies. Join us in creating the ultimate horror movie guide!

