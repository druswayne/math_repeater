from aiogram import Bot, Dispatcher, Router
import sqlite3
from config.config import TOKEN
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

con = sqlite3.connect("config/data.db")
cursor = con.cursor()
router = Router()

dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)

user_data = {}
user_data_day = {}
user_data_not_start = {}
