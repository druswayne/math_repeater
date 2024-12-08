import json
import requests
from aiogram import Bot, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from keys.keys import kb_settings, kb_exit_menu
from loader import router, cursor, con


@router.message(F.text == 'Статистика')
async def get_settings(message: Message, bot: Bot, state: FSMContext):
    id_user = message.chat.id
    with open(f'data/user_json/{id_user}.json', 'r', encoding='utf-8') as file:
        data_file = json.loads(file.read())
    try:
        text = (
            f'Повторений за тренировку – {round(sum(data_file['count_cards_in_day']) / len(data_file['count_cards_in_day']), 2)}\n'
            f'Время тренировки: {round(sum(data_file['count_times_in_day']) / len(data_file['count_times_in_day']), 2)}\n'
            )
    except:
        text = (
            f'Повторений за тренировку – {0}\n'
            f'Время тренировки: {0}\n'
            )

    builder = ReplyKeyboardBuilder()
    for button in kb_exit_menu:
        builder.add(button)
    builder.adjust(2)
    await message.answer(text,reply_markup=builder.as_markup(resize_keyboard=True))
