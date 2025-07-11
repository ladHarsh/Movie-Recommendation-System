import pickle
import streamlit as st
import requests


API_KEY = "TMDB api key"
FALLBACK_POSTER = "https://via.placeholder.com/500x750.png?text=No+Image"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        if response.status_code != 200:
            return FALLBACK_POSTER
        data = response.json()
        poster_path = data.get("poster_path")
        if not poster_path:
            return FALLBACK_POSTER
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    except:
        return FALLBACK_POSTER


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.set_page_config(layout="wide")
st.title('🎬 Movie Recommender System')

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
