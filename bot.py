import json
import logging
import asyncio

from num2words import num2words

from loader import *
import datetime
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from handlers import start
from handlers import settings
from handlers import edit_settings
from handlers import training_start
from handlers import training
from handlers import stats
from handlers import add_sc
from handlers import del_user
from scripts.add_scropt import add



async def main():
    scheduler.start()
    add(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(filename='errors.log',level=logging.ERROR)

    asyncio.run(main())