from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import emoji
from utils.db_api.db_commands import get_categories, get_users, get_questions, count_items, get_cur_shift, \
    count_done_in_cat, check_done

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "user", "category", "question_id", "res")


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, user='0', category='0', question_id='0', res=0):
    return menu_cd.new(level=level, user=user,
                       category=category, question_id=question_id, res=res)


# Создаем функцию, которая отдает клавиатуру с доступными сменами
async def shifts_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    users = await get_users()
    for user in users:
        button_text = user.name
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, user=user.id)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text='➕ Добавить пользователя',
            callback_data='add_user'
        ))
    return markup


# Клавиатура со списком категорий
async def categories_keyboard():
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await get_categories()
    cur_shift = await get_cur_shift()
    for cat in categories:
        count = await count_items(cat.category)
        count_done = await count_done_in_cat(cur_shift, cat.category)
        button_text = f'{cat.category} ({count_done}/{count})'
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=cat.category)
        markup.insert(InlineKeyboardButton(
            text=button_text, callback_data=callback_data
        ))
    markup.row(
        InlineKeyboardButton(
            text=f"{emoji.emojize(':red_circle:')} Завершить смену",
            callback_data='finish_shift'
        ))
    return markup


# Клавиатура со списком вопросов
async def questions_keyboard(category):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    # Забираем список категорий из базы данных
    questions = await get_questions(category)
    cur_shift = await get_cur_shift()
    for q in questions:
        if await check_done(cur_shift,q.id):
            button_text = '✅ '+q.text
        else:
            button_text = q.text
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, question_id=q.id)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, question_id='dummy'))
    )
    return markup


# Клавиатура с результатом айтема T/F
def item_keyboard(category, question_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
        text=f'{emoji.emojize(":thumbs_up:")} OK',
        callback_data=make_callback_data(level=CURRENT_LEVEL - 2, res=True)
    ))
    markup.insert(InlineKeyboardButton(
        text=f'{emoji.emojize(":thumbs_down:")} Не ОК',
        callback_data=make_callback_data(level=CURRENT_LEVEL - 2, res=False)
    ))
    return markup
