# TODO: 
# [+] write parse_rooms function
# [ ] write parse_groups function
# [ ] write parse_lecturers function
# [ ] something else
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url_rooms = "https://www.alt.ranepa.ru/shedule/rooms/"

def get_page(url: str) -> "http.client.HTTPResponse":
    return urlopen(url)

def make_soup(html: "http.client.HTTPResponse") -> "BeautifulSoup":
    return bs(html, 'html.parser')

def parse_rooms(soup: "BeautifulSoup") -> list:
    cooked_soup = soup.find_all("div", "b-schedule__border-list")
    digested_dict = {} 

    for ingredients in cooked_soup:
        for ingredient in ingredients.find_all('li'):
            digested_dict[ingredient.text] = "https://www.alt.ranepa.ru" + str(ingredient.find('a').get('href'))

    return digested_dict




if __name__ == "__main__":
    parse_rooms(make_soup(get_page(url_rooms)))


