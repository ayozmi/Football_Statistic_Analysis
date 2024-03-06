# file: fetch_api_data.py
import requests

def fetch_data(api_endpoint):
    """ Fetch data from the given API endpoint. """
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == "__main__":
    api_url = 'YOUR_API_ENDPOINT_HERE'
    data = fetch_data(api_url)
    # Process the data or save it to a file/DB