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
@router.message(Command('repeat'))
async def repeat_sc(message: Message, bot: Bot):
    user_id  = message.chat.id
    scheduler.remove_all_jobs()
    if user_id == 731866035:
        dir_files = os.listdir('data/user_json')
        for file in dir_files:
            if 'sample' not in file:
                with open(f'data/user_json/{file}', 'r', encoding='utf-8') as file_:
                    data = json.loads(file_.read())
                id_user = data['id_user']
                sc = scheduler.add_job(scheduler_training, trigger='cron', hour=data['time_training'].split(':')[0],
                                       minute=data['time_training'].split(':')[1], kwargs={'bot': bot, 'id_user': id_user})
                cursor.execute('update users set id_scheduler=(?)', (sc.id,))
                con.commit()

        await bot.send_message(chat_id=user_id, text='ok')
