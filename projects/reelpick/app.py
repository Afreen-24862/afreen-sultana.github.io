"""
ReelPick - Step 5: Streamlit web app
====================================
Run with:  streamlit run app.py
Streamlit re-runs this script from top to bottom on every click, so the
heavy work (loading data) is cached and the UI code stays very short.
"""
import streamlit as st

from recommend import _data, recommend

st.set_page_config(page_title="ReelPick", page_icon="🎬", layout="centered")
st.title("🎬 ReelPick")
st.caption("Content-based movie recommendations - TMDB 5000 dataset")


@st.cache_data                     # load the title list once per session
def all_titles():
    movies, _, _ = _data()
    return sorted(movies["title"].tolist())


# --- Inputs -------------------------------------------------------------
titles = all_titles()
choice = st.selectbox("Pick a movie you like", titles,
                      index=titles.index("The Dark Knight Rises"))
col1, col2 = st.columns(2)
n = col1.slider("How many suggestions?", 3, 10, 5)
min_votes = col2.slider("Minimum votes (quality filter)", 0, 2000, 200, 100)

# --- Output -------------------------------------------------------------
if st.button("Recommend", type="primary"):
    title, picks = recommend(choice, n=n, min_votes=min_votes)
    if not picks:
        st.warning("No matches above the vote filter - try lowering it.")
    st.subheader(f"Because you liked {title}")
    for p in picks:
        with st.container(border=True):
            left, right = st.columns([4, 1])
            left.markdown(f"**{p['title']}** ({p['year']})  \n{p['genres']}")
            right.metric("Match", f"{p['match']:.0%}")
            st.progress(min(p["match"] * 2, 1.0))   # visual similarity bar
            st.caption(f"⭐ {p['rating']:.1f} / 10")
