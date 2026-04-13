import streamlit as st
import requests

st.title("ANO KABA? LAGAY MO NA ANG KANTA.")

if "results" not in st.session_state:
    st.session_state.results = []

query = st.text_input("Enter a song title here:")
submit = st.button("Submit")

if submit and query:
    url = "https://lrclib.net/api/search"
    params = {"q": query}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        st.session_state.results = response.json()
    else:
        st.error("Failed to fetch songs.")

if st.session_state.results:
    result = st.session_state.results

    song_options = []
    for song in result:
        artist = song.get('artist') or song.get('artistName') or 'Unknown Artist'
        title = song.get('name') or song.get('title') or 'Unknown'
        song_options.append(f"{title} - {artist}")

    selected_song = st.selectbox("Select a song:", song_options)

    selected_index = song_options.index(selected_song)
    song = result[selected_index]

    artist = song.get('artist') or song.get('artistName') or 'Unknown Artist'
    title = song.get('name') or song.get('title') or 'Unknown'

    st.subheader(f"🎵 {title} - {artist}")

    song_id = song.get("id")

    if song_id:
        lyrics_url = f"https://lrclib.net/api/get/{song_id}"

        try:
            with st.spinner("Loading lyrics...."):
                lyrics_response = requests.get(lyrics_url)

            if lyrics_response.status_code == 200:
                lyrics_data = lyrics_response.json()
                lyrics_text = lyrics_data.get('plainLyrics') or lyrics_data.get('syncedLyrics')

                if lyrics_text:
                    st.text_area("Lyrics:", value=lyrics_text, height=400, disabled=True)
                else:
                    st.info("Lyrics not available for this song.")

        except Exception as e:
            st.error(f"Error fetching lyrics: {str(e)}")