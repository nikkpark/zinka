# -*- coding: utf-8 -*- 
import random
import datetime

def phrase():
    file = open('truth.txt', 'r')
    raw_text = file.read()
    file.close()

    text_list = raw_text.split('_')
    #while True:    
    #    question = input('Задавай свой вопрос, странник!\n')
    #    num = len(question)
    #    random.seed(datetime.datetime.now())
    #    i = random.randint(0, len(text_list)-1)
    #    print('Таков мой тебе ответ!\n', text_list[i])
    #    print()
    random.seed(datetime.datetime.now())
    i = random.randint(0, len(text_list))
    return text_list[i]
