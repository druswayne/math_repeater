import json
import random
from importlib.metadata import files
from num2words import num2words
from keys.keys import kb_training_start, kb_training_ckeck, kb_training_next, kb_training_end
from loader import router, user_data, user_data_day, user_data_not_start
from aiogram import F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, WebAppInfo, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import requests
from json import loads
import time


@router.callback_query(F.data.startswith("training"))
async def open_table(callback: types.CallbackQuery, bot: Bot):
    callback_data = callback.data.split('_')[1]
    id_user = callback.message.chat.id
    data = user_data[id_user]
    if callback_data == "start":
        user_data_not_start[id_user] = True
        kb = kb_training_ckeck
        url = user_data[id_user][1][0]
        user_data[id_user][5] = True
        user_data[id_user][3] = url
        user_data[id_user][4] = time.time()
        file = FSInputFile(url)

    elif callback_data == 'check':
        with open(f'data/user_json/{id_user}.json', 'r', encoding='utf-8') as file:
            data_file = json.loads(file.read())
        data_file['files'][user_data[id_user][3]] += 1
        with open(f'data/user_json/{id_user}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data_file))

        user_data[id_user][1].remove(user_data[id_user][3])
        user_data[id_user][2] += 1
        file_name = user_data[id_user][3].split('/')
        name_file = file_name[-1].replace('on', 'of')
        file_name[-1] = name_file
        new_file = '/'.join(file_name)
        file = FSInputFile(new_file)
        if not len(user_data[id_user][1]):
            kb = kb_training_end
        else:
            kb = kb_training_next
    elif callback_data == 'next':
        if not len(user_data[id_user][1]):
            del user_data[id_user]
            await bot.delete_message(chat_id=id_user, message_id=callback.message.message_id)
            print('xyi')
            text_message = ('Тренировка завершена!\n'
                            f'Повторений за тренировку: {user_data[id_user][2] - len(user_data[id_user][1])}\n'
                            f'Время тренировки: {int((time.time() - user_data[id_user][4]) // 60)} мин {int((time.time() - user_data[id_user][4]) % 60)} сек')
            await callback.message.answer(text_message)
            return
        kb = kb_training_ckeck
        url = random.choice(user_data[id_user][1])
        user_data[id_user][3] = url
        file = FSInputFile(url)
    elif callback_data == 'end':
        if user_data[id_user][5]:


            with open(f'data/user_json/{id_user}.json', 'r', encoding='utf-8') as file:
                data_file = json.loads(file.read())
            data_file['count_cards_in_day'].append(user_data[id_user][2])
            data_file['count_times_in_day'].append(round((time.time() - user_data[id_user][4]) / 60, 2))
            if user_data_day[id_user] == "scheduler":
                data_file['nostop_day'] += 1



            try:
                sr_znach = round(sum(data_file['count_cards_in_day']) / len(data_file['count_cards_in_day']), 2)

            except:
                sr_znach = 0


            if int(time.time() - user_data[id_user][4]) < 10:

                text_message = ('Мне кажется ты жульничаешь, так быстро нельзя было завершить тренировку!\n'
                                'Постарайся так больше не делать.')
                if user_data_day[id_user] == "scheduler":
                    data_file['nostop_day'] = 0

            else:
                text_message = 'Тренировка завершена!\n'
                if user_data_day[id_user] == "scheduler":
                    text_message+= f'Ежедневных тренировок подряд: {data_file['nostop_day']}\n'
                if user_data[id_user][2] > sr_znach:
                    text_message+= f'Сегодня ты поработал лучше обычного!\n'
                else:
                    text_message+=f'Сегодня ты поработал чуть хуже обычного\n'

                text_message+=f'Повторений за тренировку: {user_data[id_user][2]}\n'
                text_message+=f'Время тренировки: {int((time.time() - user_data[id_user][4]) // 60)} мин {int((time.time() - user_data[id_user][4]) % 60)} сек'
            del user_data_day[id_user]
            with open(f'data/user_json/{id_user}.json', 'w', encoding='utf-8') as file:
                                    file.write(json.dumps(data_file))
        else:
            text_message = 'Тренировка завершена!\n'
        await bot.delete_message(chat_id=id_user, message_id=callback.message.message_id)
        await callback.message.answer(text_message)
        del user_data[id_user]
        del user_data_not_start[id_user]
        return

    builder = InlineKeyboardBuilder()
    for button in kb:
        builder.add(button)

    builder.adjust(1)

    await bot.edit_message_media(message_id=callback.message.message_id, chat_id=id_user,
                                 media=types.InputMediaPhoto(media=file, caption=''), reply_markup=builder.as_markup())
