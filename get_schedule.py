# TODO: 
# [+] write parse_rooms function
# [+] write parse_groups function
# [+] write parse_lecturers function
# [+] design parse_lesson data collection structure
# [ ] write parse_lessons function
# [ ] something else

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

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

    for i in digested_dict.items():
        print(i)
    return digested_dict


def parse_lessons(entity_identifier: str, url: str) -> dict:
    room_pattern = re.compile('^[А|В|Б|а|б|в|A|B|a|b]\d')
    group_pattern = re.compile('^[0-9][0-9]')
    lecturer_pattern = re.compile('^[А-Я|а-я][а-я]')

    if re.match(room_pattern, entity_identifier):
        cooked_lessons = make_soup(get_page(url)) 
        lessons_list = cooked_lessons.find_all('div', 'b-schedule__table-group')
        lessons_room = cooked_lessons.find('div', 'b-schedule__header-title').text
        lessons = [] 

        lesson_days = cooked_lessons.find_all('div', 'b-schedule__table-title')
        for day in lesson_days:
            lessons.append({day.text : []})

        

        
        



        

    elif re.match(group_pattern, entity_identifier):
        pass
    elif re.match(lecturer_pattern, entity_identifier):
        pass
    else:
        return -1

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
    weekdays_soup = cooked_lessons.find_all('div', 'b-schedule__table')
    weekdays_soup = weekdays_soup[1:]
    weekdays_list = []

    for i in range(len(weekdays_soup)):
        weekdays_list.append(weekdays_soup[i].find('div','b-schedule__table-title').text)



if __name__ == "__main__":
    #parse_rooms_and_groups(make_soup(get_page(url_groups)))
    #parse_lecturers(make_soup(get_page(url_lecturers)))
    parse_lessons('A101', 'https://www.alt.ranepa.ru/shedule/rooms/room101/')
