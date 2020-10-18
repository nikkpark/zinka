from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime


def getPage(url):
    return urlopen(url)

def parsePage(html):
    return BeautifulSoup(html, 'html.parser')

def collectData(bsObj):
    """
        CONTENT STRUCTURE (MAKE A JSON?)
        wrapper{'day':[['time', 'title', 'room'], [another one lecture]],
                'day':[[and another one lecture]],
                'etc...'
                }
    """
    raw_days = bsObj.find('section').findAll('div', {'class':'b-schedule__table--teacher'})    
    days = {}

    for day in raw_days:
        day_name = day.find('div', {'class':'b-schedule__table-title'}).text
        if day.find('div', {'class':'b-schedule__table-row--blue'}) in day:            
            lect_properties_tmp = []            
            for lecture in day.findAll('div', {'class':'b-schedule__table-row--blue'}):                              
                for lect_property in lecture.findAll('div', {'class':'b-schedule__table-item'})[1:-1]:
                    if lect_property.find('span') in lect_property:
                        lect_properties_tmp.append(lect_property.find('span').text.replace("\xa0", ''))                        
                    else:
                        lect_properties_tmp.append(lect_property.text.strip())          
            days[day_name] = lect_properties_tmp

    return days

def printOut(days_dict):
    print()
    for day in days_dict:        
        print('В ' + day + ' в ' + days_dict[day][0][:6] + 'у директора лекция '
                + days_dict[day][2] + ' в аудитории ' + days_dict[day][3] + '.')
        print()
        
def makeMessage(days_dict):
    if len(days_dict) != 0:
        messages = []
        for day in days_dict:        
            message = 'В ' + day + ' в ' + days_dict[day][0][:6] + 'у директора лекция ' + days_dict[day][2] + ' в аудитории ' + days_dict[day][3] + '.'
            messages.append(message)
    else:
        messages = ["Нет лекций."]
    return messages

def saveAsPic(some_output):
    pass

def run():
    if datetime.datetime.today().weekday() == 6:
        a = datetime.datetime.today() + datetime.timedelta(days=1)
        url = 'http://www.alt.ranepa.ru/shedule/lecturers/lect21/' + str(a)[:10]
    else:
        url = 'http://www.alt.ranepa.ru/shedule/lecturers/lect21/'

    page = getPage(url)
    bsObj = parsePage(page)
    days = collectData(bsObj)
    return makeMessage(days)
    #printOut(days)

if __name__ == '__main__':
    run()
