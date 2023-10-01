import streamlit as st
import mysql.connector
import pandas as pd

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'imdb_top_250'
)
mycursor = database.cursor()
mycursor.execute('USE IMDB_TOP_250')

st.title('Movies Filter by Years of Produce')
years = list(range(1900, 2024))
start_col, end_col = st.columns(2)
start_year = start_col.selectbox('from', [''] + years)
end_year = end_col.selectbox('to', [''] + years)

if start_year != '' and end_year != '':
    query = f"SELECT title, Runtime, Parental_guide FROM movie WHERE Year BETWEEN {start_year} AND {end_year}"
    mycursor.execute(query)
    result = mycursor.fetchall()
    if result:
        st.header(f'Movies produced between {start_year} and {end_year}')
        dataframe = pd.DataFrame(result, columns=["Title", "Runtime (hours)", "Parental Guide"])
        st.table(dataframe)
    else:
        st.warning('DUUUUUUUDEEEEE I cant find ')

st.title('Movies Duration')
start_col, end_col = st.columns(2)
time_start = start_col.number_input('Enter Minimum Time:', min_value=0, max_value=1000)
time_end = end_col.number_input('Enter Maximum Time:', min_value=0, max_value=1000)
if time_start is not None and time_end is not None and time_start <= time_end:
    query = f"SELECT title, Year, Parental_guide FROM movie WHERE Runtime BETWEEN {time_start} AND {time_end}"
    mycursor.execute(query)
    result = mycursor.fetchall()

    if result:
        st.header(f'Movies Duration {time_start} and {time_end}')
        dataframe = pd.DataFrame(result, columns=["Title", "Year", "Parental Guide"])
        st.table(dataframe)
    else:
        st.warning('No movies found within the specified duration.')
elif time_start is not None or time_end is not None:
    st.warning('Please enter valid values for both time.')

st.title("Filter by celebrity name")
star_names = []
num_star_fields = st.number_input("How many stars do you want to add?", min_value=1, value=1)
for i in range(num_star_fields):
    star_name = st.text_input(f"Star Name {i + 1}")
    star_names.append(star_name)
if st.button("Search"):
    query = """
    SELECT movie.Title
    FROM movie
    INNER JOIN cast ON movie.id = cast.Movie_id
    INNER JOIN person ON cast.Person_id = person.id
    WHERE person.name IN (%s)
    """
    placeholders = ', '.join(['%s' for _ in star_names])
    query = query % placeholders

    mycursor.execute(query, tuple(star_names))
    results = mycursor.fetchall()
    if results:
        dataframe = pd.DataFrame(results, columns=["Movie Title"])
        st.table(dataframe)
    else:
        st.info("But Go Watch Insterstellar")

database.close()

