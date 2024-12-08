from aiogram import Bot, types, F
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keys.keys import kb_training_start
from loader import json, router, user_data
import os
import time


async def scheduler_training(bot: Bot, id_user):
    with open(f'data/user_json/{id_user}.json', 'r', encoding='utf-8') as file:
        data_file = json.loads(file.read())
    file_path = data_file['files']
    files = sorted(file_path, key=file_path.get)
    #file_path = []
    #for tema in data_file['tems']:
    #    folder = f'data/class/class_7/{tema}'
    #    files_in_folder = os.listdir(folder)
    #    for file in files_in_folder:
    #        if 'of' not in file:
    #            file_path.append(f'{folder}/{file}')


    builder = InlineKeyboardBuilder()
    for button in kb_training_start:
        builder.add(button)
    builder.adjust(1)
    url = 'data/start.png'
    file = FSInputFile(url)
    await bot.send_photo(chat_id=id_user, caption='Что дальше?',
                                         photo=file,
                                   reply_markup=builder.as_markup(resize_keyboard=True))
    user_data[id_user] = [0, files ,0, 0, 0, False ]


