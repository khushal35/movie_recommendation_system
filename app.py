import streamlit as st
import pickle
import pandas as pd
import requests

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommend_movies = []
    recommend_posters = []

    for i in movies_list:
        movie_id =  movies.iloc[i[0]].id

        recommend_movies.append(
            movies.iloc[i[0]].title
        )
        #fetch poster from api
        recommend_posters.append(
            fetch_poster(movie_id)
        )

    return recommend_movies, recommend_posters

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=56c2b3152e53da573e7ad31b12710117"

    response = requests.get(url)
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie recommender System')
selected_movie_name=st.selectbox (
    'Choose a movie to recommend'
    ,movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

    for i in range(5):
        st.write(names[i])
        st.image(posters[i])

