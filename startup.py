# startup.py

"""
This script is designed to run as part of a Dockerized application setup.
It waits for the Flask backend service to become available and then makes
a POST request to the /add_the_witch route to add a movie to the database.
"""

import time
import requests


def wait_for_server(url, timeout=60):
    """
    Wait for the server to be available by making GET requests to the URL.

    :param url: URL of the server to check.
    :param timeout: Maximum time in seconds to wait for the server.
    :raises Exception: If the server is not up within the timeout.
    """
    start_time = time.time()
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Server is up and running.")
                break
        except requests.exceptions.ConnectionError:
            print("Server is not yet available. Waiting...")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}.")

        time_elapsed = time.time() - start_time
        if time_elapsed > timeout:
            raise Exception(f"Server did not start within {timeout} seconds.")

        time.sleep(1)  # wait a second before checking again


def add_movie(url):
    """
    Makes a POST request to the given URL to add a movie to the database.

    :param url: URL to which the POST request will be made.
    :return: The response text from the POST request.
    """
    try:
        response = requests.post(url)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"An error occurred while adding the movie: {e}."


def main():
    """
    Main execution function to wait for the server and add a movie.
    """
    # URL of the Flask application
    flask_url = (
        "http://backend:8000"  # Use the service name as defined in docker-compose
    )

    # Wait for the Flask server to start
    wait_for_server(flask_url)

    # URL for adding the movie
    add_movie_url = f"{flask_url}/add_the_witch"

    # Make the POST request to add the movie
    result = add_movie(add_movie_url)
    print(result)


if __name__ == "__main__":
    main()
