from aiogram.utils.keyboard import ReplyKeyboardBuilder

from loader import router, cursor, con
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keys.keys import kb_menu

class Form_name(StatesGroup):
    name = State()

@router.message(F.text == 'Меню')
@router.message(Command('start'))
async def reg(message: Message, bot: Bot, state: FSMContext) -> None:
    print(message.chat.id)
    id_user = message.chat.id
    cursor.execute('select * from users where id=(?)', (id_user,))
    data = cursor.fetchall()
    if not len(data):
        cursor.execute('insert into users (id) values (?)', (id_user,))
        con.commit()
        await state.set_state(Form_name.name)
        await message.answer('Как к тебе обращаться?')
    else:
        builder = ReplyKeyboardBuilder()
        for button in kb_menu:
            builder.add(button)
        builder.adjust(2)
        await message.answer(text='Что дальше?',
                             reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(Form_name.name)
async def get_name(message: Message, bot, state: FSMContext):
    await state.update_data(name=message.text)
    data_name = await state.get_data()
    name = data_name['name']
    cursor.execute('UPDATE users SET name=(?)', (name,))
    con.commit()
    await state.clear()
    await message.answer(f'Добро пожаловать {name}!')
