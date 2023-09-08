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

st.title("Top 10 Highest-Grossing Movies")

if st.button("Show Chart"):
    query = """
    SELECT movie.Title, movie.Gross_us_canada
    FROM movie
    ORDER BY movie.Gross_us_canada DESC
    LIMIT 10
    """

    mycursor.execute(query)
    results = mycursor.fetchall()

    if results:
        movie_titles = [result[0] for result in results]
        gross_values = [result[1] for result in results]
        plt.figure(figsize=(10, 6))
        plt.barh(movie_titles, gross_values)
        plt.xlabel("Gross (in billions)")
        plt.gca().invert_yaxis() 
        st.pyplot(plt)
    else:
        st.info("No movie data found.")

    st.title("Top 5 Busiest Actors")

    query = """
    SELECT person.Name, COUNT(*) AS movie_count
    FROM cast
    INNER JOIN person ON cast.Person_id = person.id
    GROUP BY person.name
    ORDER BY movie_count DESC
    LIMIT 5
    """

    mycursor.execute(query)
    results = mycursor.fetchall()

    if results:
        df = pd.DataFrame(results, columns=["Actor", "Movie Count"])
        plt.figure(figsize=(10, 6))
        plt.barh(df["Actor"], df["Movie Count"])
        plt.xlabel("Number of Movies")
        plt.gca().invert_yaxis() 

        st.pyplot(plt)


    st.title("Movie Genre Distribution")

    query = """
    SELECT Genre, COUNT(*) AS genre_count
    FROM genre_movie
    GROUP BY Genre
    """

    mycursor.execute(query)
    results = mycursor.fetchall()

    if results:
        df = pd.DataFrame(results, columns=["Genre", "Count"])
        plt.figure(figsize=(8, 8))
        plt.pie(df["Count"], labels=df["Genre"], autopct="%1.1f%%", startangle=140)
        st.pyplot(plt)



    st.title("Movie Age Rating Distribution")

    query = """
    SELECT Parental_guide, COUNT(*) AS count
    FROM movie
    GROUP BY Parental_guide
    """

    mycursor.execute(query)
    results = mycursor.fetchall()

    if results:
        df = pd.DataFrame(results, columns=["Parent guid", "Count"])
        plt.figure(figsize=(8, 8))
        plt.pie(df["Count"], labels=df["Parent guid"], autopct="%2f%%", startangle=140)
        st.pyplot(plt)



    st.title("Age Rating Distribution in Each Genre")
    query = """
    SELECT Genre, Parental_guide, COUNT(*) AS rating_count
    FROM genre_movie
    INNER JOIN movie ON genre_movie.Movie_id = movie.id
    GROUP BY Genre, Parental_guide
    """

    mycursor.execute(query)
    results = mycursor.fetchall()

    if results:
        df = pd.DataFrame(results, columns=["Genre", "Age Rating", "Count"])
        pivot_df = df.pivot(index="Age Rating", columns="Genre", values="Count").fillna(0)
        plt.figure(figsize=(24, 10))
        pivot_df.plot(kind="bar", stacked=True)
        plt.xlabel("Age Rating")
        plt.ylabel("Count")
        st.pyplot(plt)
