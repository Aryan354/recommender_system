import streamlit as st
import pickle
import pandas as pd
import requests


def poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=df9378c399b89b9285f340cfc42ea2fa&language=en-US'.format(
        movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster(movie_id))
    return recommended_movies, recommended_movie_posters


similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = pickle.load(open('movie_d.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

st.title('KHerum?')

selected_movie = st.selectbox(
    'Which movie is on your mind?',
    movies['title'])

if st.button('Recommend'):
    names, movie_poster = recommend(selected_movie)
    cols = st.columns(5, gap="medium")
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(movie_poster[i])


