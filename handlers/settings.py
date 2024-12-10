import json
import requests
from aiogram import Bot, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from keys.keys import kb_settings
from loader import router, cursor, con


@router.message(F.text == 'Настройки')
async def get_settings(message: Message, bot: Bot, state: FSMContext):
    id_user = message.chat.id
    cursor.execute('select * from users where id=(?)', (id_user,))
    user_ = cursor.fetchall()
    if not user_:
        await message.answer('Используй /start для регистрации')
        return
    try:
        with open(f'data/user_json/{id_user}.json', 'r', encoding='utf-8') as file:
            data_file = json.loads(file.read())
        text = (f'Класс – {' ,'.join(data_file['class'])}\n'
                f'Темы для повторения: \n✅{"\n✅".join(data_file["tems"])}\n'
                f'Время тренировки: {data_file["time_training"]}')
    except:
        text = 'Для начала необходимо настроить план занятий'

    builder = ReplyKeyboardBuilder()
    for button in kb_settings:
        builder.add(button)
    builder.adjust(2)
    await message.answer(text,reply_markup=builder.as_markup(resize_keyboard=True))
