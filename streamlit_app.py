import streamlit as st
import pandas as pd
import sqlite3
import base64

def load_data():
    """Load data from the SQL database."""
    conn = sqlite3.connect('/path/to/database.sqlite')  # Update this path
    df = pd.read_sql_query("SELECT * FROM statistics", conn)
    conn.close()
    return df

def set_background(png_file):
    """Set a background image for the Streamlit app."""
    with open(png_file, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    set_background('streamlit_app/assets/2022-04-18.jpg')  # Ensure correct path
    st.title('Football Statistic Analysis', anchor=None)

    with st.container():
        styled_container = f"""
        <style>
            .stContainer {{
                background-color: rgba(255, 255, 255, 0.5); /* Semi-transparent white */
                border-radius: 15px;
                padding: 10px;
            }}
        </style>
        """
        st.markdown(styled_container, unsafe_allow_html=True)
        
        # Load and display the data within the styled container
        df = load_data()
        st.write(df)
        
        # Display a video from a URL within the styled container
        st.video('https://www.youtube.com/watch?v=0eOf-EOCzuw')
        
        # Display the UEFA banner at the bottom of the page within the styled container
        st.image('streamlit_app/assets/uefa_banner.png', use_column_width=True)
        
        # Additional app content goes here

if __name__ == '__main__':
    main()
