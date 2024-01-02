"""
startup.py
----------

This script is designed to run as part of a Dockerized application setup.
It's responsible for ensuring that the Flask backend service is available by making
GET requests to the service's URL. Once the service is confirmed to be available,
it makes a POST request to a specified route (e.g., '/search_trailers') to perform an action
such as adding trailers to the database.

This script is typically executed after the service it depends on is known to have started.
"""

import time
import requests


def wait_for_server(url, timeout=60):
    """
    Continuously checks if the server at the provided URL is available by making GET requests.

    Parameters:
    - url (str): URL of the server to check.
    - timeout (int): Maximum time in seconds to wait for the server.

    Raises:
    - TimeoutError: If the server is not up within the timeout period, indicating the server
      might be down or not yet ready.

    This function will announce when the server is up and running and break out of its
    checking loop, or raise a TimeoutError if the server doesn't become available in the
    specified time.
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
            raise TimeoutError(f"Server did not start within {timeout} seconds.")

        time.sleep(1)  # Wait a second before retrying


def add_movie(url):
    """
    Sends a POST request to the specified URL intended to trigger an action such as
    adding a movie or trailers to the database.

    Parameters:
    - url (str): URL to which the POST request will be made.

    Returns:
    - str: The response text from the POST request, typically a confirmation message or
           details of the added movie/trailer.

    If the request encounters an exception, it will return a descriptive error message.
    """
    request_timeout = 5  # Timeout for the post request
    try:
        response = requests.post(url, timeout=request_timeout)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"An error occurred while adding the movie: {e}"


def main():
    """
    The main execution function. Orchestrates waiting for the Flask server to be available
    and then making a POST request to a designated URL to perform an action such as adding
    trailers.

    The specific action and URL are determined by the configuration of the Flask application
    and may involve adding a single movie, a batch of trailers, or any other POSTable action.
    """
    # URL of the Flask application
    flask_url = "http://backend:8000"

    # Wait for the Flask server to start with the specified timeout
    wait_for_server(flask_url)

    # URL for the action to be taken, e.g., adding trailers
    add_movie_url = f"{flask_url}/search_trailers"

    # Make the POST request to take action
    result = add_movie(add_movie_url)
    print(result)


if __name__ == "__main__":
    main()
