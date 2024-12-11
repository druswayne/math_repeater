from aiogram import Bot, types, F
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from keys.keys import kb_training_start
from loader import json, router, user_data, user_data_day, user_data_not_start, cursor
import os
import time


async def scheduler_training(bot: Bot, id_user):

    cursor.execute('select * from users where id=(?)', (id_user,))
    user_ = cursor.fetchall()
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
    user_data_day[id_user] = "scheduler"
    message = await bot.send_photo(chat_id=id_user, caption=f'{user_[0][1]}, ты готов позаниматься?',
                                         photo=file,
                                   reply_markup=builder.as_markup(resize_keyboard=True))
    user_data[id_user] = [0, files ,0, 0, 0, False ]
    user_data_not_start[id_user] = False
    await asyncio.sleep(600)
    if not user_data_not_start[id_user]:

        await message.delete()
        del user_data[id_user]
        with open(f'data/user_json/{id_user}.json', 'r', encoding='utf-8') as file:
            data_file = json.loads(file.read())
        data_file['nostop_day'] = 0
        with open(f'data/user_json/{id_user}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data_file))
        del user_data_not_start[id_user]
        await bot.send_message(chat_id=id_user, text=(f'{user_[0][1]}, ты пропустил сегодня тренировку 🦥\n'
                                                         'Постарайся придерживайся плана 📋'))





