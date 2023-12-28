"""
startup.py

This script is designed to run as part of a Dockerized application setup.
It waits for the Flask backend service to become available by making
GET requests to the service's URL. Once the service is available, it
makes a POST request to the '/add_the_witch' route to add a movie to the
database.
"""

import time
import requests


def wait_for_server(url, timeout=60):
    """
    Wait for the server to be available by making GET requests to the URL.

    Parameters:
    - url (str): URL of the server to check.
    - timeout (int): Maximum time in seconds to wait for the server.

    Raises:
    - Exception: If the server is not up within the timeout period.
    """
    start_time = time.time()
    request_timeout = 5  # Timeout for each individual request attempt
    while True:
        try:
            response = requests.get(url, timeout=request_timeout)
            if response.status_code == 200:
                print("Server is up and running.")
                break
        except requests.exceptions.ConnectionError:
            print("Server is not yet available. Waiting...")
        except requests.exceptions.Timeout:
            print("Server response timed out.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}.")

        if time.time() - start_time > timeout:
            raise Exception(f"Server did not start within {timeout} seconds.")

        time.sleep(1)  # Wait a second before retrying


def add_movie(url):
    """
    Makes a POST request to the given URL to add a movie to the database.

    Parameters:
    - url (str): URL to which the POST request will be made.

    Returns:
    - str: The response text from the POST request.
    """
    request_timeout = 5  # Timeout for the post request
    try:
        response = requests.post(url, timeout=request_timeout)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"An error occurred while adding the movie: {e}"


def main():
    """
    Main execution function that orchestrates waiting for the server to be available
    and then adding a movie.
    """
    # URL of the Flask application
    flask_url = "http://backend:8000"

    # Wait for the Flask server to start with the specified timeout
    wait_for_server(flask_url)

    # URL for adding the movie
    add_movie_url = f"{flask_url}/add_the_witch"

    # Make the POST request to add the movie
    result = add_movie(add_movie_url)
    print(result)


if __name__ == "__main__":
    main()
