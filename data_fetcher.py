import requests

API_KEY = 'PWX0kgVn0wVUz5uMdQ5RcA==jpQKyNFSCzKizpbz'
REQUEST_URL = f'https://api.api-ninjas.com/v1/animals?name='
HEADERS = {'X-Api-Key': API_KEY}


def fetch_data(animal_name):
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals, each animal is a dictionary:
    {
      'name': ...,
      'taxonomy': {
        ...
      },
      'locations': [
        ...
      ],
      'characteristics': {
        ...
      }
    },
    """
    api_url = REQUEST_URL + animal_name
    response = requests.get(api_url, headers=HEADERS)
    return response.json()
