import requests


def scrap_url(url: str, fn: str) -> None:
    """
    Scrapes the content from the provided URL and saves it to a text file.

    Args:
        url (str): The URL of the webpage to scrape.
        fn (str): The filename where the webpage content will be saved.

    Returns:
        None
    """
    try:
        r = requests.get(url)

        # Check if the response was successful (status code 200)
        r.raise_for_status()  # Will raise an exception if status code is not 200 (success)

        with open(fn, 'w', encoding='utf-8') as file:
            file.write(r.text)
        print(f"Page successfully scrapped into {fn}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")

    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")

    except requests.exceptions.TooManyRedirects as redirects_err:
        print(f"Too many redirects: {redirects_err}")

    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")


url = 'https://www.google.com'
fn = 'scrapped_page.txt'

scrap_url(url, fn)
