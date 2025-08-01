import streamlit as st
import os
from analyze_game import analyze_pgn

st.set_page_config(page_title="Chess Coach Agent", layout="centered")

st.title("♟️ Chess Coach Agent")
st.markdown("Upload a PGN file to analyze your game and get feedback from Gemini AI.")

# Upload PGN file
uploaded_file = st.file_uploader("Upload your PGN file", type=["pgn"])

if uploaded_file is not None:
    temp_file_path = os.path.join("temp.pgn")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded. Starting analysis...")

    with st.spinner("Analyzing your game with Stockfish + Gemini..."):
        try:
            from analyze_game import analyze_pgn
            analyze_pgn(temp_file_path)
            st.success("Done!")
        except Exception as e:
            st.error(f"Error during analysis: {e}")

