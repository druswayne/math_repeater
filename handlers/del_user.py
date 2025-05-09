import json

from aiogram.utils.keyboard import ReplyKeyboardBuilder
import os
from loader import router, cursor, con, scheduler
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keys.keys import kb_menu
from scripts.scheduler_training import scheduler_training
@router.message(Command('delete'))
async def delete_user(message: Message, bot: Bot):
    user_id  = message.chat.id

    cursor.execute('select id_scheduler from users where id=(?)',(user_id,))
    id_scheduler = cursor.fetchall()[0][0]
    if len(str(id_scheduler)) != 0 and id_scheduler is not None:
        scheduler.remove_job(id_scheduler)
    file_path = f'data/user_json/{user_id}.json'
    if os.path.isfile(file_path):
        os.remove(file_path)
    cursor.execute('delete from users where id=(?)', (user_id,))
    con.commit()
    await message.answer('Вы успешно удалили свой профиль')