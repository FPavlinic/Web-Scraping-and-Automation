# used libraries
from bs4 import BeautifulSoup
import requests

# url to web page with list of top 100 movies
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# go to the url and get HTML
response = requests.get(URL)
eo_webpage = response.text
soup = BeautifulSoup(eo_webpage, "html.parser")

# get list of movie titles from HTML
movie_titles = [movie.getText() for movie in soup.find_all(name="h3", class_="title")]
# reverse list to order movies from best to worst
movie_titles.reverse()

# create txt file to save list of top 100 movies
with open("movies.txt", mode="w") as movies_file:
    for movie in movie_titles:
        movies_file.write(f"{movie}\n")
