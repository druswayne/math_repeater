import json
from idlelib.iomenu import encoding
from random import shuffle

import requests
from aiogram import Bot, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from keys.keys import kb_settings, kb_menu
from loader import router, cursor, con, scheduler
from scripts.scheduler_training import scheduler_training
import os

def get_directories_dict(root_dir):
    directories_dict = {}
    for root, dirs, _ in os.walk(root_dir):
        if os.path.basename(root).startswith('class_'):
            directories_dict[os.path.basename(root)] = dirs
    return directories_dict

@router.message(F.text == 'Сменить параметры')
async def edit_settings(message: Message, bot:Bot):
    id_user = message.chat.id
    cursor.execute('select * from users where id=(?)', (id_user,))
    user_ = cursor.fetchall()
    if not user_:
        await message.answer('Используй /start для регистрации')
        return

    root_directory = 'data/class/'
    directories_dict = get_directories_dict(root_directory)
    data = json.dumps({'id_user': id_user, "tems": directories_dict})
    requests.post('https://xata6bl4.pythonanywhere.com/', json=data)
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='открыть', web_app=WebAppInfo(
        url=f"https://xata6bl4.pythonanywhere.com/form/?id_user={id_user}")))
    builder.adjust(4)
    await bot.send_message(chat_id=id_user,
                           text='Выбрать параметры',
                           reply_markup=builder.as_markup(resize_keyboard=True),
                           )


def remove_empty_lists(d):
    return {k: v for k, v in d.items() if v}

@router.callback_query(F.data == "end_setting")
async def get_data(callback: types.CallbackQuery, bot: Bot):

    id_user = callback.message.chat.id


    url = f'https://xata6bl4.pythonanywhere.com/static/{id_user}.json'
    data = json.loads(requests.get(url).text)

    data['tems'] = remove_empty_lists(data['tems'])

    with open('data/user_json/sample.json', 'r', encoding='utf-8') as file:
        data_sample = json.loads(file.read())
    data_sample['id_user'] = id_user
    data_sample['time_training'] = data['time']
    for i in data['tems']:
        data_sample['class'].append(i.replace('klass_class_', ''))
        data_sample['tems'] += data['tems'][i]
    # если не выбрал ничего, отмена и заново
    files_ = {}
    for klass in data_sample['class']:
        directories = data['tems'][f'klass_class_{klass}']
        shuffle(directories)
        for folder in directories:
            path = f'data/class/class_{klass}/{folder}'
            directories_files = os.listdir(path)
            shuffle(directories_files)
            for file_ in directories_files:
                if 'of' not in file_ :
                    files_[f'data/class/class_{klass}/{folder}/{file_}'] = 0
    data_sample['files'] = files_



    with open(f'data/user_json/{id_user}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data_sample))
    cursor.execute('select id_scheduler from users where id=(?)',(id_user,))
    id_scheduler = cursor.fetchall()[0][0]
    if len(str(id_scheduler)) != 0 and id_scheduler is not None:
        scheduler.remove_job(id_scheduler)
    id_message = callback.message.message_id
    await bot.delete_message(chat_id=id_user, message_id=id_message)
    builder = ReplyKeyboardBuilder()
    for button in kb_menu:
        builder.add(button)
    builder.adjust(2)

    sc = scheduler.add_job(scheduler_training, trigger='cron', hour=data['time'].split(':')[0], minute=data['time'].split(':')[1], kwargs={'bot': bot, 'id_user':id_user})
    cursor.execute('update users set id_scheduler=(?)', (sc.id,))
    con.commit()
    await callback.message.answer(text='Настройки сохранены!',
                         reply_markup=builder.as_markup(resize_keyboard=True))



