import json
import random
import speech_recognition as sr
from moviepy.editor import AudioFileClip
from num2words import num2words
from pyexpat.errors import messages
import os
from keys.keys import kb_training_start, kb_training_ckeck, kb_training_next, kb_training_end, kb_training_answer, \
    kb_training_answer_voice
from loader import router, user_data, user_data_day, user_data_not_start, cursor, con
from aiogram import F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, WebAppInfo, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import requests
from json import loads
import time


class FormVoice(StatesGroup):
    voice = State()
    url = State()


@router.callback_query(F.data.startswith("training"))
async def open_table(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    callback_data = callback.data.split('_')[1]
    id_user = callback.message.chat.id
    cursor.execute('select * from users where id=(?)', (id_user,))
    user_ = cursor.fetchall()

    if not user_:
        await callback.message.answer('Используй /start для регистрации')
        return

    data = user_data[id_user]
    if callback_data == "start":
        user_data_not_start[id_user] = True
        kb = kb_training_ckeck
        url = user_data[id_user][1][0]
        user_data[id_user][5] = True
        user_data[id_user][3] = url
        user_data[id_user][4] = time.time()
        file = FSInputFile(url)
    elif callback_data == 'voice':

        await state.update_data(url=user_data[id_user][3])
        await state.set_state(FormVoice.voice)

        await bot.edit_message_caption(message_id=callback.message.message_id, chat_id=id_user,
                                       caption='Отправь свой ответ голосовым сообщением, а я проверю!'
                                       )
        return
    elif callback_data == 'check':
        with open(f'data/user_json/{id_user}.json', 'r', encoding='utf-8') as file:
            data_file = json.loads(file.read())
        data_file['files'][user_data[id_user][3]] += 1
        with open(f'data/user_json/{id_user}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data_file))

        file_name = user_data[id_user][3].split('/')
        name_file = file_name[-1].replace('on', 'of')
        file_name[-1] = name_file
        new_file = '/'.join(file_name)
        file = FSInputFile(new_file)
        kb = kb_training_answer
    elif callback_data == 'true' or callback_data == 'false':

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
                cursor.execute('update users set counter_day = counter_day + 1')
                con.commit()

            try:
                sr_znach = round(sum(data_file['count_cards_in_day']) / len(data_file['count_cards_in_day']), 2)

            except:
                sr_znach = 0

            if int(time.time() - user_data[id_user][4]) < 10:

                text_message = (f'{user_[0][1]}, мне кажется ты жульничаешь!\nТренировка не может быть такой быстрой,\n'
                                'постарайся так больше не делать.')
                if user_data_day[id_user] == "scheduler":
                    cursor.execute('update users set counter_day = 0')
                    con.commit()

            else:
                text_message = 'Тренировка завершена 🎉\n'
                if user_data_day[id_user] == "scheduler":

                    cursor.execute('select counter_day from users where id = (?)', (id_user,))
                    counter_day = cursor.fetchall()[0][0]
                    if counter_day in [1, 3, 5, 10, 20]:
                        url_num_img = f'data/img_num/{counter_day}.png'
                        file_num_image = FSInputFile(url_num_img)
                        num_day = num2words(counter_day, to='ordinal', lang='ru', gender='f')
                        text_message += f'Сегодня {num_day} тренировка подряд, так держать!🏆\n'
                        await callback.message.answer_photo(caption=text_message, photo=file_num_image)
                        text_message = ''
                    else:
                        num_day = num2words(counter_day, to='ordinal', lang='ru', gender='f')
                        text_message += f'Сегодня уже {num_day} тренировка подряд, так держать!🏆\n'
                    if user_data[id_user][2] >= sr_znach:
                        text_message += f'{user_[0][1]}, сегодня тебе удалось поработать лучше обычного 📈\n'
                    else:
                        text_message += f'{user_[0][1]}, сегодня тебе удалось поработать чуть хуже обычного 📉\n'
                text_message += '\nСтатистика тренировки:\n'

                text_message += f'Повторений за тренировку: {user_data[id_user][2]}💪\n'
                text_message += f'Время тренировки: {int((time.time() - user_data[id_user][4]) // 60)} мин {int((time.time() - user_data[id_user][4]) % 60)} сек ⏳'
            del user_data_day[id_user]
            with open(f'data/user_json/{id_user}.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps(data_file))
        else:

            if user_data_day[id_user] == "scheduler":
                cursor.execute('update users set counter_day = 0')
                con.commit()
                text_message = (f'{user_[0][1]}, ты пропустил сегодняшнюю тренивку.\n'
                                'Помни, дисциплина залог успеха!')
            else:
                text_message = f'{user_[0][1]}, тренировка закончилась, даже не начавшись.\n'

        await bot.delete_message(chat_id=id_user, message_id=callback.message.message_id)
        await callback.message.answer(text_message)
        try:
            del user_data[id_user]
            del user_data_not_start[id_user]
        except:
            pass
        return

    builder = InlineKeyboardBuilder()
    for button in kb:
        builder.add(button)

    builder.adjust(2)

    await bot.edit_message_media(message_id=callback.message.message_id, chat_id=id_user,
                                 media=types.InputMediaPhoto(media=file, caption=''), reply_markup=builder.as_markup())


from openai import OpenAI


@router.message(FormVoice.voice)
@router.message(F.voice)
async def get_voice(message: Message, bot, state: FSMContext):
    file_id = message.voice.file_id

    file = await bot.get_file(file_id)

    file_path = file.file_path

    ogg_path = f'temp/{message.chat.id}.ogg'

    await bot.download_file(file_path, ogg_path)

    # Конвертируем в WAV используя moviepy
    audio_clip = AudioFileClip(ogg_path)

    wav_path = f'temp/{message.chat.id}.wav'

    audio_clip.write_audiofile(wav_path, fps=44100)

    audio_clip.close()

    # Распознаем речь
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data, language='ru-RU')

    if os.path.exists(ogg_path):
        os.remove(ogg_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)

    data = await state.get_data()
    await state.clear()
    url = data['url']
    data = url.split('/')
    data[1] = 'answer'
    num = int(data[-1].split('_')[0])
    data[-1] = f'{num}.txt'
    answer_url = '/'.join(data)
    with open(answer_url, 'r', encoding='utf-8') as file:
        data_answer = file.read()

    client = OpenAI(
        api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI2YzIzN2MwLWJmZmMtNGNiZC1hYTVhLTAwZDQ2OWUyZDZmZCIsImlzRGV2ZWxvcGVyIjp0cnVlLCJpYXQiOjE3NDQ5OTI5OTcsImV4cCI6MjA2MDU2ODk5N30.-xE7_Ts_v3tTYibxr7tXwrteYjHtE_HnyVs7hEI7Thk',
        base_url='https://bothub.chat/api/v2/openai/v1'
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': (f"""Ты учитель математики в средней школе. Ученик отвечает тебе на вопрос.
сильно не придирайся, ты добрый учитель. 
Твоя задача сравнить ответ ученика  с текстом правильного ответа (текс ответа содержит всю необходимую информацию, которую ученик должен даь), и кратко прокоментировать ответ ученику.
Комментарий ты даешь от своего лица и обращаешься к ученику (не используй в обращении слово ученик. 
в комментарии ты должен сказать, правильно ли ответил ученик на вопрос. если ответил с грубыми ошибками, то указать на них.
ответ ученика может быть не слово в слово, главное, чтобы было по смыслу правильно. 
ты можешь добавлять в конце какую-то доп информацию по вопросу в конце обращения."""
                            f'Ответ ученика:{text}'
                            f'Правильный ответ:{data_answer}')
            }
        ],
        model='o3-mini-high',
    )

    result = chat_completion.choices[0].message.content

    id_user = message.from_user.id
    with open(f'data/user_json/{id_user}.json', 'r', encoding='utf-8') as file:
        data_file = json.loads(file.read())
    data_file['files'][user_data[id_user][3]] += 1
    with open(f'data/user_json/{id_user}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data_file))

    file_name = user_data[id_user][3].split('/')
    name_file = file_name[-1].replace('on', 'of')
    file_name[-1] = name_file
    new_file = '/'.join(file_name)
    file = FSInputFile(new_file)

    builder = InlineKeyboardBuilder()
    for button in kb_training_next:
        builder.add(button)

    builder.adjust(2)
    await message.delete()
    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_media(message_id=i, chat_id=id_user,
                                         media=types.InputMediaPhoto(media=file, caption=result),
                                         reply_markup=builder.as_markup())
            break
        except:
            pass
