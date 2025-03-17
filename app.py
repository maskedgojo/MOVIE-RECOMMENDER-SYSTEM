import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    # **REPLACE WITH YOUR ACTUAL API KEY**
    api_key = "YOUR_ACTUAL_API_KEY"
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ebc4f3cd5f472e3ac88e17e4ae901bdb&language=en-US')
    data = response.json()
    #st.text(data)  #Good for debugging
    #st.text(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US') #Good for debugging

    # Check if the request was successful
    if response.status_code == 200 and 'poster_path' in data:
        return "https://image.tmdb.org/t/p/original/" + data['poster_path']
    else:
        return "https://via.placeholder.com/150"  # Return a placeholder image if there's an error

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        # fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))  # Call fetch_poster
    return recommended_movies, recommended_movies_posters # Return both lists as a tuple

# Load data
try:
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Make sure 'movies.pkl' and 'similarity.pkl' are in the same directory as your script.")
    st.stop()

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Use st.columns instead of st.beta_columns (deprecated)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0], use_column_width=True)
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1], use_column_width=True)
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2], use_column_width=True)
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3], use_column_width=True)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4], use_column_width=True)
