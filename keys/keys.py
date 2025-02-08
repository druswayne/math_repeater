from aiogram import types
from aiogram.types import WebAppInfo

kb_menu = [
    #types.KeyboardButton(text='Быстрая тренировка'),
    types.KeyboardButton(text='Статистика'),
    types.KeyboardButton(text='Параметры')
]

kb_settings = [
    types.KeyboardButton(text='Сменить параметры'),
    types.KeyboardButton(text='Меню')]

kb_exit_menu = [
    types.KeyboardButton(text='Меню')]

kb_training_answer = [
    types.InlineKeyboardButton(text="Ответил верно 👍", callback_data="training_true"),
    types.InlineKeyboardButton(text="Ответил неверно 👎", callback_data="training_false"),
    types.InlineKeyboardButton(text="Закончить", callback_data="training_end")]

kb_training_start = [
    types.InlineKeyboardButton(text="Начать", callback_data="training_start"),
    types.InlineKeyboardButton(text="Закончить", callback_data="training_end")]

kb_training_ckeck = [
    types.InlineKeyboardButton(text="Проверить", callback_data="training_check"),
    types.InlineKeyboardButton(text="Закончить", callback_data="training_end")]

kb_training_next = [
    types.InlineKeyboardButton(text="Следующий", callback_data="training_next"),
    types.InlineKeyboardButton(text="Закончить", callback_data="training_end")]

kb_training_end = [
    types.InlineKeyboardButton(text="Закончить", callback_data="training_end")]
