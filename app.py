import pickle
import streamlit as st
import requests

# ✅ Streamlit UI
st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎥", layout="wide")

# 🎨 Custom CSS
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1524985069026-dd778a71c7b4");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;

        }

        .stApp h1, .stApp h3 {
            color: white !important;
        }

        .movie-card {
    text-align: center;
    margin-top: 10px;
    padding: 10px;
    background-color: lightgreen !important;  /* force yellow */
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.movie-title {
    margin-top: 8px;
    font-size: 20px;
    font-weight: bold;
    color: #000 !important;  /* force black text */
}


        /* 🎯 Button Styling */
        .stButton > button {
            background-color: #ffcc00;
            color: #000;
            border-radius: 10px;
            padding: 8px 16px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: darkgreen !important;
            color: black !important;
            font-weight:bold;
        }
    </style>
""", unsafe_allow_html=True)

import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f43230da1c21f2ef6f6f45c55f5fc51a".format(movie_id)
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # raise error if invalid
        data = response.json()
        st.text(data)
        st.text("https://api.themoviedb.org/3/movie/{}?api_key=f43230da1c21f2ef6f6f45c55f5fc51a".format(movie_id))
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except Exception as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/500x750?text=Poster+Not+Available"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].get('movie_id')
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters



movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# 🖥️ Streamlit UI
st.title("🎬 Movie Recommender System")
st.markdown("### ⭐ Find similar movies you’ll love!")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendations 🚀"):
    names, posters = recommend(selected_movie)
    if names:
        cols = st.columns(len(names))
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f"""
                    <div class="movie-card">
                        <img src="{posters[idx]}" width="150" style="border-radius:10px;">
                        <div class="movie-title">{names[idx]}</div>
                    </div>
                """, unsafe_allow_html=True)
