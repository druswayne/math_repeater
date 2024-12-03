from aiogram import Bot, Dispatcher, Router
import sqlite3
from config.config import TOKEN
import json
con = sqlite3.connect("data.db")
cursor = con.cursor()
router = Router()

dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)

user_data = {}