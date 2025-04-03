from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_connect import Connect
import random
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio


CHANNEL_ID = "@EnglishBreakthrough" 

class CheckWord(StatesGroup):
    word = State()
    stat = State()

db = Connect()
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id

    # Проверяем подписку пользователя
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    if chat_member.status not in ['member', 'administrator', 'creator']:
        # Если пользователь не подписан, показываем сообщение с кнопкой
        ikb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔗 Подписаться на канал", url=f"https://t.me/{CHANNEL_ID.strip('@')}")],
                [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subscription")]
            ]
        )
        await message.answer(
            "⚠️ Чтобы использовать бота, подпишитесь на канал и нажмите 'Проверить подписку'.",
            reply_markup=ikb
        )
        return

    # Если пользователь подписан, показываем главное меню
    await send_main_menu(message, bot, user_id)


@router.callback_query(F.data == "check_subscription")
async def check_subscription(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    user_name = call.from_user.first_name if call.from_user.first_name else "Гость"  # Получаем имя пользователя
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        await call.message.delete()
        await call.message.answer("✅ Вы подписались! Теперь можете пользоваться ботом.")
        await send_main_menu(call.message, bot, user_id, user_name)
    else:
        await call.answer("Вы всё ещё не подписаны. Подпишитесь на канал и попробуйте снова.", show_alert=True)



async def send_main_menu(message: Message, bot: Bot, user_id: int, user_name: str):
    # Проверяем, есть ли пользователь в базе
    check_user = db.cur.execute("SELECT * FROM statistics WHERE user_id = ?", (user_id,)).fetchone()
    if not check_user:
        db.create_user(user_id, user_name)

    # Создаем кнопки главного меню
    ikb = InlineKeyboardBuilder()
    ikb.button(text='🎮 Играть', callback_data='start_game_cb')
    ikb.button(text='📊 Посмотреть статистику', callback_data='check_stat_cb')
    ikb = ikb.adjust(1).as_markup()

    # Отправляем приветствие с именем пользователя
    await message.answer(
        f'Привет, {user_name}!\n\n'
        'Нажми <u>Играть</u>, чтобы запустить викторину:',
        parse_mode='HTML',
        reply_markup=ikb
    )


# Кнопка для перехода в главное меню во время игры
@router.callback_query(F.data == 'main_menu_cb')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    ikb = InlineKeyboardBuilder()
    ikb.button(text='🎮 Играть', callback_data='start_game_cb')
    ikb.button(text='📊 Посмотреть статистику', callback_data='check_stat_cb')
    ikb = ikb.adjust(1).as_markup()
    await call.message.answer(f'Вы в главном меню. Выберите, что хотите сделать:', reply_markup=ikb)
    await call.answer()

@router.callback_query(lambda message: message.data == 'start_game_cb')
async def start_game(call: CallbackQuery, state: FSMContext):
    words = db.get_words()
    right_word = words[random.randint(0, 3)]
    words_ikb_builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки для слов
    for kb in words:
        words_ikb_builder.button(text=kb[2], callback_data=str(kb[0]))
    
    # Добавляем кнопку для перехода в главное меню
    words_ikb_builder.button(text='🏠 Главное меню', callback_data='main_menu_cb')
    words_ikb_builder.adjust(2)  # Расставляем кнопки по две в ряд

    await state.set_state(CheckWord.word)
    await state.update_data(word=right_word)

    words_ikb = words_ikb_builder.as_markup()
    await call.message.answer(f'💬 Как переводится слово <b>{right_word[1]}</b>?\n\nТекущий уровень: {db.get_stat(call.from_user.id)[2]}', reply_markup=words_ikb, parse_mode='HTML')
    await call.answer()

@router.callback_query(CheckWord.word)
async def right_answer(call: CallbackQuery, bot: Bot, state: FSMContext):
    right_word = await state.get_data()
    right_word = right_word['word']
    await state.clear()
    await call.message.delete()

    # Проверим, был ли правильный ответ
    if call.data == str(right_word[0]):
        await call.message.answer(f'✅ Абсолютно верно! <b>{right_word[1]}</b> переводится как <b>{right_word[2]}</b>', parse_mode='HTML')
        db.update_right(call.from_user.id)
    else:
        await call.message.answer(f'❌ Не верно! <b>{right_word[1]}</b> переводится как <b>{right_word[2]}</b>', parse_mode='HTML')
        db.update_wrong(call.from_user.id)

    # Обновим уровень и проверим, изменился ли он
    level_increased, new_level = db.update_level(call.from_user.id)

    # Если уровень увеличился, поздравим пользователя
    if level_increased:
        await call.message.answer(f'🎉 Ваш уровень повышен! Вы достигли уровня {new_level}! Поздравляем! 🏅')

    await bot.send_chat_action(call.from_user.id, action='typing')
    await start_game(call, state)

@router.callback_query(F.data == 'check_stat_cb')
async def get_stat(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    answers = db.get_stat(call.from_user.id)

    ikb = InlineKeyboardBuilder()
    ikb.button(text='🎮 Продолжить играть', callback_data='start_game_cb')
    ikb.button(text='🧹 Отчистить статистику', callback_data='clear_stat_cb')
    ikb.adjust(1)
    ikb = ikb.as_markup()
    await call.message.answer(f'📊 Ваша статистика:\n\n'
                             f'💬 Всего дано ответов - {answers[0] + answers[1]}\n'
                             f'✅ Количество правильных - {answers[0]}\n'
                             f'❌ Количество ошибок - {answers[1]}\n'
                             f'🏅 Ваш уровень - {answers[2]}', reply_markup=ikb)

@router.callback_query(F.data == 'clear_stat_cb')
async def clear_stat_cmd(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    db.clear_stat(call.from_user.id)
    await call.message.answer('Статистика успешно обновлена.')
    await get_stat(call, state)

@router.message()
async def handle_unknown_command(message: Message):
    await message.answer("Извините, такой команды не существует. Используйте /start для начала.")
