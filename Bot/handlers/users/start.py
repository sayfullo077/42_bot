from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters.state import State, StatesGroup
from api import create_user, get_all_users, update_user
from loader import dp, bot
from aiogram import types, html
import asyncio
import random
import time
import re
import logging
import html

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    check_exist = State()
    check = State()

user_cache = {}

BASE_URL = "http://127.0.0.1:8000/api/v1"


def html_escape(text):
    escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return re.sub(r'[&<>"\']', lambda match: escape_chars[match.group(0)], text)


async def check_cache():
    while True:
        current_time = time.time()
        for user_id, (code, timestamp) in list(user_cache.items()):
            if current_time - timestamp > 60:
                del user_cache[user_id]
        await asyncio.sleep(10)


async def prompt_for_contact(message: types.Message, full_name: str):
    await message.answer(
        f"Hello {full_name}! \nShare your contact for registration and you will be given a special code!"
    )
    phone_button = types.KeyboardButton(text="Share Contact", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[phone_button]])
    await message.answer("Please share your contact with us:", reply_markup=keyboard)


@dp.message(CommandStart())
async def start(message: types.Message):
    user = message.from_user
    user_id = str(user.id)
    full_name = html_escape(user.full_name)

    try:
        users = get_all_users()

        if not users:
            await prompt_for_contact(message, full_name)
            logging.info("No users found; prompting for contact.")
        else:
            user_exists = any(existing_user['user_id'] == user_id for existing_user in users)

            if user_exists:
                await message.answer("You have an old code, you can update it with the /login command!")
            else:
                await prompt_for_contact(message, full_name)
                logging.info("User not found; prompting for contact.")

    except Exception as e:
        logging.error(f"Error in start function: {e}")


@dp.message(lambda message: message.contact)
async def handle_contact(message: types.Message):
    user = message.from_user
    user_id = user.id
    contact = message.contact.phone_number
    code = random.randint(100000, 999999)
    user_cache[user_id] = (code, time.time())        
        
    try:
        users = get_all_users()
        if not users:
            await message.answer(f"🔒 Code:\n<pre>{html.escape(str(code))}</pre>", parse_mode="HTML")
            response_message = create_user(user.username, user.first_name, contact=contact, user_id=user_id, code=code)
            await message.answer(response_message, reply_markup=ReplyKeyboardRemove())
            logging.info("User created.")
        else:
            user_exists = any(existing_user['user_id'] == user_id for existing_user in users)
            if user_exists:
                response_message = update_user(user_id, code)
                await message.answer(f"🔒 Your new code is:\n<pre>{html.escape(str(code))}</pre>", parse_mode="HTML")
                await message.answer(response_message)
                logging.info(f"User updated: {response_message}")
                
            else:
                await message.answer(f"🔒 Code:\n<pre>{html.escape(str(code))}</pre>", parse_mode="HTML")
                response_message = create_user(user.username, user.first_name, contact=contact, user_id=user_id, code=code)
                await message.answer(response_message, reply_markup=ReplyKeyboardRemove())
            

    except Exception as e:
        logging.error(f"Error in handle_contact function: {e}")

@dp.message(Command("login"))
async def login_command(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"User cache: {user_cache}")

    try:
        users = get_all_users()
        user_ids = [int(user['user_id']) for user in users]
        if user_id not in user_ids:
            await message.answer("Your ID was not found, please register.")
            return
        
        if user_id in user_cache:
            code, timestamp = user_cache[user_id]
            current_time = time.time()
            
            if current_time - timestamp <= 60:
                await message.answer(f"🔒 Your valid code:\n<pre>{html.escape(str(code))}</pre>", parse_mode="HTML")

            else:
                await generate_new_code(message, user_id)
        else:
            await generate_new_code(message, user_id)

    except Exception as e:
        logging.error(f"Error in login_command function: {e}")
        await message.answer(f"An error occurred. Please try again : {e}")

async def generate_new_code(message: types.Message, user_id: int):
    code = random.randint(100000, 999999)
    user_cache[user_id] = (code, time.time())
    response_message = update_user(user_id, code)

    await message.answer(f"🔒 Your new code:\n<pre>{html.escape(str(code))}</pre>", parse_mode="HTML")
    await message.answer(response_message)