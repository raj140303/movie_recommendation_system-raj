import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id): 
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=00047d05e40d2f3b2ccf4cc638fe3017&language=en-US")
    data = response.json()
    
    if data and "poster_path" in data and data["poster_path"]:  
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"  

# Recommendation function
def recommend(movie):
    try:
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommend_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            if "movie_id" in movies.columns:  # Ensure column exists
                movie_id = movies.iloc[i[0]].movie_id  
                recommended_movies_posters.append(fetch_poster(movie_id))  
            else:
                recommended_movies_posters.append("https://via.placeholder.com/500x750.png?text=No+Movie+ID")

            recommend_movies.append(movies.iloc[i[0]].title)  

        return recommend_movies, recommended_movies_posters  

    except Exception as e:
        st.error(f"Oops! Something went wrong: {str(e)}")
        return [], []

# Load movie data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Page styling and header updates
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #8A2BE2;
            text-align: center;
            margin-top: 20px;
        }
        .recommend-header {
            font-size: 24px;
            font-weight: bold;
            color: #8A2BE2;
            text-align: center;
            margin-bottom: 20px;
        }
        .movie-list {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }
        .movie-item {
            position: relative;
            width: 100%;
            height: 350px;  /* Adjusted height */
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }
        .movie-item img {
            width: 100%;  /* Width is set to 100% */
            height: auto;  /* Height is set to auto to preserve aspect ratio */
            object-fit: cover;  /* Ensures the image covers the area without distortion */
        }
        .movie-item:hover {
            transform: scale(1.05);
        }
        .movie-name {
            position: absolute;
            bottom: 10px;
            left: 10px;
            font-size: 18px;
            font-weight: 600;
            color: white;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.6);
            background-color: rgba(0, 0, 0, 0.5);
            padding: 8px;
            border-radius: 5px;
        }
        .sticker {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 50%;
            padding: 8px;
        }
        .sticker img {
            width: 28px;
            height: 28px;
        }
        .selectbox {
            font-size: 16px;
            font-weight: normal;
            padding: 10px;
            background-color: #333;
            color: white;
            border-radius: 5px;
            width: 100%;
            margin-bottom: 20px;
        }
        .button {
            background-color: #8A2BE2;
            padding: 12px 20px;
            border-radius: 6px;
            font-weight: 600;
            color: white;
            border: none;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
        }
        .button:hover {
            background-color: #7A1EC3;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="title">🎬 Movie Recommender System</p>', unsafe_allow_html=True)     # ise attractive banao 

# Movie selection dropdown
selected_movie_name = st.selectbox(
    "Which movie would you love to see?",      # ise bhi  attractive banao
    movies["title"].values,
    key="movie_selector",
    help="Select a movie from the list to get recommendations."
)

# Recommend movies button
if st.button("Recommend", key="recommend_button"):   # is button ko attractive bana na he aur col
    names, posters = recommend(selected_movie_name)

    if names:
        # Display results in grid format
        st.markdown('<p class="recommend-header">Recommended Movies🍿</p>', unsafe_allow_html=True)
        cols = st.columns(len(names))  # Dynamic column count based on recommendations
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f'<div class="movie-item"><img src="{posters[idx]}" alt="{names[idx]}"><div class="movie-name">{names[idx]}</div></div>', unsafe_allow_html=True)
    else:
        st.warning("No recommendations found. Try selecting another movie.")
