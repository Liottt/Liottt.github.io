import telebot
from telebot import types
import os
from pytube import YouTube
token = '1488557474:AAEN5iqY6Ga0GbdIc3mMSC8tDMV11gtmuvU'
bot = telebot.TeleBot(token, parse_mode=None)

keyboard = types.InlineKeyboardMarkup()
mp3 = types.InlineKeyboardButton(text="Аудиофайл", callback_data="MP3")
mp4 = types.InlineKeyboardButton(text="Видеофайл", callback_data="MPEG4")
keyboard.add(mp3, mp4)
@bot.message_handler(commands=['start'], content_types=['text'])
def start_bot(message):
    bot.send_message(message.chat.id, "Вас приветсвует IZZI бот!\nВыберите формат файла для скачивания с Youtube:",
                     reply_markup=keyboard)


def retry_bot(message):
    bot.send_message(message.chat.id, "Хотите скачать что-то еще?\nВыберите формат файла для скачивания с Youtube:",
                     reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call, message):
    if call.data == "MP3":
        bot.send_message(message.chat.id, "Введите ссылку для Аудиофайла:")
        bot.register_next_step_handler(message.chat.id, mp3_dl)
    elif call.data == "MPEG4":
        bot.send_message(message.chat.id, "Введите ссылку для Видеофайла:")
        bot.register_next_step_handler(message.chat.id, mp4_dl)

def mp3_dl(message):
    try:
        yt = YouTube(message.text)
        bot.send_message(message.chat.id, "Загрузка началась")
        yt.streams.filter(only_audio=True).download()
        bot.send_message(message.chat.id, "Загрузка закончилась! Подождите конвертируем файл...")
        os.replace(f"{os.getcwd()}\{yt.title}.mp4", f"{os.getcwd()}\{yt.title}.mp3")
        open(f"{os.getcwd()}\{yt.title}.mp3", "rb")
        bot.send_audio(message.chat.id, f"{os.getcwd()}\{yt.title}.mp3")
        (f"{os.getcwd()}\{yt.title}.mp3", "rb").close()
        os.remove(f"{os.getcwd()}\{yt.title}.mp3")
        bot.register_next_step_handler(message.chat.id, retry_bot)
    except:
        bot.send_message(message.chat.id, "Введите корректную ссылку!")
        bot.register_next_step_handler(message.chat.id, mp3_dl)

def mp4_dl(message):
    try:
        yt = YouTube(message.text)
        bot.send_message(message.chat.id, "Загрузка началась")
        yt.streams.get_highest_resolution().download()
        bot.send_message(message.chat.id, "Загрузка закончилась!\nПодождите конвертируем файл...")
        open(f'{os.getcwd()}\{yt.title}.mp4', 'rb')
        bot.send_video(message.chat.id, (f'{os.getcwd()}\{yt.title}.mp4', 'rb'))
        (f'{os.getcwd()}\{yt.title}.mp4', 'rb').close()
        os.remove(f'{os.getcwd()}\{yt.title}.mp4')
        bot.register_next_step_handler(message.chat.id, retry_bot)
    except:
        a = bot.send_message(message.chat.id, "Введите корректную ссылку!")
        bot.register_next_step_handler(a, mp4_dl)

if __name__=="__main__":
    bot.polling(True)