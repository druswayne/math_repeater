from aiogram import Bot, Dispatcher, Router, F
import sqlite3
from config import TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json

con = sqlite3.connect("data.db")
cursor = con.cursor()
router = Router()

dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)

user_data = {}