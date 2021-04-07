import json
from bs4 import BeautifulSoup
import requests

URL = "https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)

website_html = response.content

soup = BeautifulSoup(website_html,"html.parser")

#Json loads converts it into dictionary
#

data = json.loads(soup.select_one("#__NEXT_DATA__").contents[0])

#print(json.dumps(data,indent=4))

#isinstance returns true if the given object has the specified datatype
def find_movies(data):
    if isinstance(data,dict):
        for k,v in data.items():
            if k.startswith("ImageMeta:"):
                yield v["titleText"]
            else:
                yield from find_movies(v)
    elif isinstance(data,list):
        for i in data:
            yield from find_movies(i)

movie_titles = []
for a in find_movies(data):
    movie_titles.append(a)

movies = movie_titles[::-1]

with open("movies.txt",mode="w") as file:
    for movie in movies:
        file.write(f"{movie}\n")

# #print(soup.prettify())
#
# all_movie_names = soup.find(name="h3",class_="jsx-4245974604")
#
# print(all_movie_names)


