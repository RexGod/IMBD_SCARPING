import matplotlib.pyplot as plt
import streamlit as st
import mysql.connector
import pandas as pd

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Sh@0831@Sh',
    database = 'imdb_top_250'
)
mycursor = database.cursor()
mycursor.execute('USE IMDB_TOP_250')
#fetch genre into select_option
st.title("Top-Selling Movies in User-Selected Genre")

query = """
SELECT DISTINCT Genre
FROM genre_movie
"""

mycursor.execute(query)
available_genres = [result[0] for result in mycursor.fetchall()]

selected_genre = st.selectbox("Select a genre:", available_genres)

query = """
SELECT movie.Title, movie.Gross_us_canada
FROM movie
INNER JOIN genre_movie ON movie.id = genre_movie.Movie_id
WHERE genre_movie.Genre = %s
ORDER BY movie.Gross_us_canada DESC
LIMIT 10
"""

mycursor.execute(query, (selected_genre,))
results = mycursor.fetchall()

if results:
    df = pd.DataFrame(results, columns=["Movie Title", "Gross"])

    plt.figure(figsize=(12, 6))
    plt.barh(df["Movie Title"], df["Gross"])
    plt.xlabel("Gross (in billions $)")
    plt.title(f"Top 10 Movies by Grossing in '{selected_genre}' Genre")
    plt.gca().invert_yaxis()

    st.pyplot(plt)
else:
    st.info(f"No movies found in the '{selected_genre}' genre.")
