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

import os

@router.message(F.text == 'Сменить параметры')
async def edit_settings(message: Message):
    id_user = message.chat.id
    #открытие веб для редактирования настроек
