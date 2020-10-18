import os
import logging
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from truth import phrase
from get_audio import get_audio
from get_photo import get_photo
from get_lessons import run

Token = ''

updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text='Is u ded lol?')

def quote(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text=phrase())
        
def lesson(update, context):
    messages = run()
    for message in messages:
        context.bot.send_message(chat_id=update.effective_chat.id,text=message)

def photo(update, context):
    get_photo()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("/home/nick/Downloads/tg_dump/pic.jpg", 'rb'))
    os.remove("/home/nick/Downloads/tg_dump/pic.jpg")


def audio(update, context):
    if ("youtube" or "youtu.be" in update.message.text):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Определяю размер...')
        file_path = get_audio(update.message.text)
        print("Success.")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Обработано. Загружаю...')
        for track in file_path:
            context.bot.send_audio(
                chat_id=update.effective_chat.id,
                audio=open(track, 'rb')
            )

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text=update.message.text)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text='Ничего не поняла. Пока понимаю только /start\n/quote\n;(')


start_handler = CommandHandler('start', start)
quote_handler = CommandHandler('quote', quote)
lesson_handler = CommandHandler('lesson', lesson)
photo_handler = CommandHandler('combolibi', photo)
unknown_handler = MessageHandler(Filters.command, unknown)
audio_handler = MessageHandler(Filters.text, audio)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(quote_handler)
dispatcher.add_handler(lesson_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(audio_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()
