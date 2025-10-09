// use axios to fetch data from tmdb
//curl --location 'https://api.themoviedb.org/3/search/movie?api_key=202cf556ed2f3cd393839ea81335542d&query=Ratatouille&language=en-US'

import axios from "axios";

const API_URL = "https://api.themoviedb.org/3";
const API_KEY = "202cf556ed2f3cd393839ea81335542d";

export async function searchMovies(query: string) {
  const response = await axios.get(`${API_URL}/search/movie`, {
    params: {
      api_key: API_KEY,
      query,
      language: "en-US",
      include_adult: false,
    },
  });
  return response.data;
}

// curl --location 'https://api.themoviedb.org/3/movie/=/reviews?api_key=202cf556ed2f3cd393839ea81335542d&language=en-US'

export async function getMovieReviews(movieId: number) {
  const response = await axios.get(`${API_URL}/movie/${movieId}/reviews`, {
    params: {
      api_key: API_KEY,
      language: "en-US",
    },
  });
  return response.data;
}
