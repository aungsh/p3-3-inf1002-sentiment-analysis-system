import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

def search_movie(query: str):
    
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": query,
        "language": "en-US",
        "page": 1,
        "include_adult": False
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"TMDB API request failed with status code {response.status_code}")
    
    return response.json()

def get_movie_details(movie_id: int):
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": api_key,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"TMDB API request failed with status code {response.status_code}")
    return response.json()

#call function from cmd line
if __name__ == "__main__":
    query = "Ratatouille"
    results = search_movie(query)
    print(results)