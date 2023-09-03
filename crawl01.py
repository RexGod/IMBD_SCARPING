# %% [markdown]
# ## First Question : scarp top 250 movie imbd with information

# %% [markdown]
# ### import libraries

# %%
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import re

# %% [markdown]
# ##### get main url

# %%
urlmain = 'https://www.imdb.com/chart/top/'


# %% [markdown]
# #### Send get request to url 

# %%
headers = {'Accept-Language': 'en-US',"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

# %%
response = requests.get(url=urlmain , headers=headers)

# %%
print(response.status_code)

# %% [markdown]
# ##### parse content

# %%
soup = BeautifulSoup(response.content, 'html.parser')

# %% [markdown]
# get link for each movies

# %%
links_250 = soup.find_all('div', class_='ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b85248f1-7 lhgKeb cli-title')

# %%
scrap_info_movies = []

# %%
session = requests.Session()
for link in links_250: 
    a_element = link.find("a")
    get_att = a_element.get('href')
    movie_urls = f"https://www.imdb.com{get_att}"
    response_each_movie = requests.get(url=movie_urls, headers=headers)
    movies_soup = BeautifulSoup(response_each_movie.content, 'html.parser')
    titles = movies_soup.find('span', class_='sc-afe43def-1 fDTGTb').text
    film_id = re.search(r'/tt(\d+)/', get_att)
    if film_id:
        film_id = film_id.group(1)
    else:
        film_id = None
    gross_us_canada_element = movies_soup.find('li', {'data-testid': 'title-boxoffice-grossdomestic'})
    gross_us_canada = None
    if gross_us_canada_element:
        span_element = gross_us_canada_element.find('span', {'class': 'ipc-metadata-list-item__list-content-item'})
        if span_element:
            gross_us_canada = span_element.text
    ul_element = movies_soup.find('ul', {'class': 'ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt'})
    years = None
    parental_guide = None
    runtime = None
    for li_element in ul_element.find_all('li', {'class': 'ipc-inline-list__item'}):
        ainner_element = li_element.find('a', {'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'})
        if ainner_element:
            href = ainner_element.get('href')
            text = ainner_element.text
            if 'releaseinfo' in href:
                years = text
            elif 'parentalguide' in href:
                parental_guide = text
        else:
            runtime = li_element.text
    genre_list = movies_soup.find_all('a', {'class': 'ipc-chip ipc-chip--on-baseAlt'})
    genre = [genre.find('span', class_='ipc-chip__text').text for genre in genre_list]
    #crew
    ul_crew = movies_soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt')
    directors = None
    stars = []
    writers = []
    person_id = []
    for li_element in ul_crew.find_all('li', {'class': 'ipc-inline-list__item'}):
        ainner_crew = li_element.find('a', {'class': 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
        if ainner_crew:
            href = ainner_crew.get('href')
            text = ainner_crew.text
            if 'tt_ov_wr' in href:
                writers.append(text)
            elif 'tt_ov_st' in href:
                stars.append(text)
            elif 'tt_ov_dr' in href:
                directors = li_element.text
            person_id_match = re.search(r'/name/nm(\d+)/', href)
            if person_id_match:
                person_ids = person_id_match.group(1)
                person_id.append(person_ids)
    scrap_info_movies.append({'title': titles,'runtime':runtime, 'parental_guide' : parental_guide, 'genre': genre, 'stars': stars, 'directors': directors, 'writers': writers , 'gross_us_canada':gross_us_canada , 'film_id':film_id,'person_id':person_id})
    time.sleep(1)

session.close()


# %%
top_250 = pd.DataFrame(scrap_info_movies)

# %%
top_250.head(50)

# %%
top_250.to_csv('top_250.csv', index=False)




