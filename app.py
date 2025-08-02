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
        f"&videoEmbeddable=true"
        f"&maxResults={max_results}&key={YOUTUBE_API_KEY}"
    )
    response = requests.get(url)
    items = response.json().get("items", [])
    return [
        {
            "title": item["snippet"]["title"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "videoId": item["id"]
        }
        for item in items
    ]

# ----------- Function to search songs -----------
def search_songs(query, max_results=10):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&videoCategoryId=10"
        f"&videoEmbeddable=true"
        f"&maxResults={max_results}&q={query}&key={YOUTUBE_API_KEY}"
    )
    response = requests.get(url)
    items = response.json().get("items", [])
    return [
        {
            "title": item["snippet"]["title"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "videoId": item["id"]["videoId"]
        }
        for item in items
    ]

# ----------- Streamlit App UI -----------
st.set_page_config(page_title="🎵 Songs Finder", layout="wide")
st.title("🎵 Latest Trending & Search Songs")
# Track which video is currently playing
if "current_video" not in st.session_state:
    st.session_state.current_video = None

# Track which video is currently playing
if "current_video" not in st.session_state:
    st.session_state.current_video = None

# Tabs for Trending and Search
tab1, tab2 = st.tabs(["🔥 Trending Songs", "🔍 Search Songs"])

# ----------- Trending Songs Tab -----------
with tab1:
    region = st.selectbox("🌍 Select Region:", ["IN", "US", "UK", "CA", "AU", "JP"])
    songs = get_trending_songs(region_code=region, max_results=9)

    cols = st.columns(3)
    for idx, song in enumerate(songs):
        with cols[idx % 3]:
            st.subheader(song["title"])

            # If this is the playing song → show player
            if st.session_state.current_video == song["videoId"]:
                st.markdown(
                    f"""
                    <iframe width="100%" height="215"
                    src="https://www.youtube.com/embed/{song['videoId']}?autoplay=1"
                    frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Show thumbnail + play button
                st.image(song["thumbnail"], use_container_width=True)
                if st.button("▶ Play", key=f"play_trend_{idx}"):
                    st.session_state.current_video = song["videoId"]
                    st.experimental_rerun()

# ----------- Search Songs Tab -----------
with tab2:
    search_query = st.text_input("Enter song or artist name:")
    if search_query:
        results = search_songs(search_query, max_results=9)

        cols = st.columns(3)
        for idx, song in enumerate(results):
            with cols[idx % 3]:
                st.subheader(song["title"])

                if st.session_state.current_video == song["videoId"]:
                    st.markdown(
                        f"""
                        <iframe width="100%" height="215"
                        src="https://www.youtube.com/embed/{song['videoId']}?autoplay=1"
                        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.image(song["thumbnail"], use_container_width=True)
                    if st.button("▶ Play", key=f"play_search_{idx}"):
                        st.session_state.current_video = song["videoId"]
                        st.rerun()

