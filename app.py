import streamlit as st
import requests

# Paste your YouTube API Key here
YOUTUBE_API_KEY = "AIzaSyADeV3ggVvo-IvkU5XyYf2SA0Zn_7Ts7_I"

# ----------- Function to get trending songs -----------
def get_trending_songs(region_code="IN", max_results=10):
    url = (
        f"https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet&chart=mostPopular"
        f"&regionCode={region_code}&videoCategoryId=10"
        f"&maxResults={max_results}&key={YOUTUBE_API_KEY}"
    )
    response = requests.get(url)
    return response.json().get("items", [])

# ----------- Function to search songs -----------
def search_songs(query, max_results=10):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&videoCategoryId=10"
        f"&maxResults={max_results}&q={query}&key={YOUTUBE_API_KEY}"
    )
    response = requests.get(url)
    return response.json().get("items", [])

# ----------- Streamlit App UI -----------
st.set_page_config(page_title="🎵 Songs Finder", layout="wide")
st.title("🎵 Latest Trending & Search Songs")

# Tabs for Trending and Search
tab1, tab2 = st.tabs(["🔥 Trending Songs", "🔍 Search Songs"])

# ----------- Trending Songs Tab -----------
with tab1:
    region = st.selectbox("🌍 Select Region:", ["IN", "US", "UK", "CA", "AU", "JP"])
    songs = get_trending_songs(region_code=region, max_results=9)

    cols = st.columns(3)
    for idx, song in enumerate(songs):
        with cols[idx % 3]:
            st.subheader(song["snippet"]["title"])
            st.image(song["snippet"]["thumbnails"]["high"]["url"], use_container_width=True)
            video_url = f"https://www.youtube.com/watch?v={song['id']}"
            st.markdown(f"[▶ Watch Song]({video_url})")

# ----------- Search Songs Tab -----------
with tab2:
    search_query = st.text_input("Enter song or artist name:")
    if search_query:
        results = search_songs(search_query, max_results=9)

        cols = st.columns(3)
        for idx, song in enumerate(results):
            with cols[idx % 3]:
                st.subheader(song["snippet"]["title"])
           
                st.image(song["snippet"]["thumbnails"]["high"]["url"], use_container_width=True)
                video_url = f"https://www.youtube.com/watch?v={song['id']['videoId']}"
                st.markdown(f"[▶ Watch Song]({video_url})")
