# TODO: 
# [+] write parse_rooms function
# [+] write parse_groups function
# [+] write parse_lecturers function
# [+] design parse_lesson data collection structure
# [ ] write parse_lessons function
# [ ] something else

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url_main = "https://www.alt.ranepa.ru"
url_rooms = "https://www.alt.ranepa.ru/shedule/rooms"
url_groups =  "https://www.alt.ranepa.ru/shedule"
url_lecturers = "https://www.alt.ranepa.ru/shedule/lecturers"

def get_page(url: str) -> "http.client.HTTPResponse":
    return urlopen(url)

def make_soup(html: "http.client.HTTPResponse") -> "BeautifulSoup":
    return bs(html, 'html.parser')

def parse_rooms_and_groups(soup: "BeautifulSoup") -> list:
    cooked_soup = soup.find_all("div", "b-schedule__border-list")
    digested_dict = {} 

    for ingredients in cooked_soup:
        for ingredient in ingredients.find_all('li'):
            if str(ingredient.find('a').get('href')).startswith('/'):
                digested_dict[ingredient.text] = url_main \
                + str(ingredient.find('a').get('href'))
            else:
                digested_dict[ingredient.text] = url_main \
                + '/' + str(ingredient.find('a').get('href'))


def parse_lecturers (soup: "BeautifulSoup") -> list:
    cooked_lecturers = soup.find_all('div', 'b-schedule__teacher-name')
    cooked_links = soup.find_all('a', 'b-schedule__teacher')

    digested_dict = {}

    for i in range(len(cooked_lecturers)):
        lecturer_name = cooked_lecturers[i].find('span').text \
        + ' ' + cooked_lecturers[i].find(text=True, recursive=False)

        lecturer_link = url_lecturers + '/' + cooked_links[i].get('href')
        digested_dict[lecturer_name] = lecturer_link

    return digested_dict


def parse_lessons(soup: "BeautifulSoup") -> dict:

    """
        {'room01' :
            {'day01' :
                [
                    {'lesson_position' : 'number(str)',
                     'lesson_time' : 'time(str)',
                     'type' : 'lesson(str),
                     'name' : 'lesson_name(str),
                     'groups' : groups(str),        ## or list?
                     'lecturer' : 'lecturer_name(str)
                     },
                    
                    {'lesson_position' : 'number(str)',
                     'lesson_time' : 'time(str)',
                     'type' : 'lesson(str),
                     'name' : 'lesson_name(str),
                     'groups' : groups(str),        ## or list?
                     'lecturer' : 'lecturer_name(str)
                     }
                ],
            'day02' :
                [
                    {'lesson_position' : 'number(str)',
                     'lesson_time' : 'time(str)',
                     'type' : 'lesson(str),
                     'name' : 'lesson_name(str),
                     'groups' : groups(str),        ## or list?
                     'lecturer' : 'lecturer_name(str)
                     },
                    
                    {'lesson_position' : 'number(str)',
                     'lesson_time' : 'time(str)',
                     'type' : 'lesson(str),
                     'name' : 'lesson_name(str),
                     'groups' : groups(str),        ## or list?
                     'lecturer' : 'lecturer_name(str)
                     }
                ]
        }
    }
    """
    pass


if __name__ == "__main__":
    #parse_rooms_and_groups(make_soup(get_page(url_groups)))
    parse_lecturers(make_soup(get_page(url_lecturers)))
