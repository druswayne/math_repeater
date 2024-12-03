import json
import random
from importlib.metadata import files

from keys.keys import kb_training_start, kb_training_ckeck, kb_training_next
from loader import router, user_data
from aiogram import F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, WebAppInfo, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import requests
from json import loads


@router.callback_query(F.data.startswith("training"))
async def open_table(callback: types.CallbackQuery, bot: Bot):
    callback_data = callback.data.split('_')[1]
    id_user = callback.message.chat.id
    data = user_data[id_user]
    if callback_data == "start":
        kb = kb_training_ckeck
        url = random.choice(data[1])
        data[3] = url
        data[1].remove(url)
        file = FSInputFile(url)

    elif callback_data == 'check':
        kb = kb_training_next
        file_name = data[3].split('/')
        name_file = file_name[-1].replace('on', 'of')
        file_name[-1] = name_file
        new_file = '/'.join(file_name)
        file = FSInputFile(new_file)

    elif callback_data == 'next':
        kb = kb_training_next
        url = random.choice(data[1])
        data[3] = url
        data[1].remove(url)
        file = FSInputFile(url)

    builder = InlineKeyboardBuilder()
    for button in kb:
        builder.add(button)

    builder.adjust(1)
    await bot.edit_message_media(message_id=callback.message.message_id,chat_id=id_user,
                                     media=types.InputMediaPhoto(media=file, caption=''),reply_markup=builder.as_markup())



