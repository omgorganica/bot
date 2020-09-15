import datetime
import logging
from pprint import pprint
from typing import Union, Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, state
from aiogram.types import CallbackQuery, Message
from states.shift_states import States
from keyboards.inline.menu_keyboards import menu_cd, shifts_keyboard, categories_keyboard, questions_keyboard, \
    item_keyboard
from loader import dp
import uuid

# Хендлер на команду /menu
from utils.db_api.db_commands import add_result, add_shift, get_cur_shift, count_positive_results, get_single_question, \
    get_user_first_name, add_user, user_exist, get_negative_results, update_shift, count_positive_results_prev_shift
from utils.misc.misc_defs import bool_res


@dp.message_handler(Command("menu"), state='*')
async def show_menu(message: types.Message, state: FSMContext):
    # Выполним функцию, которая отправит пользователю кнопки с доступными сменами
    await list_shifts(message)
    await States.shift_start.set()
    await add_shift()
    shift_id = await get_cur_shift()
    async with state.proxy() as data:
        data['shift_id'] = shift_id


async def list_shifts(message: types.Message, **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await shifts_keyboard()
    await message.answer("Добрый день, представьтесь пожалуйста", reply_markup=markup)


# Функция, которая отдает кнопки с категорями
async def list_categories(callback: CallbackQuery, state: FSMContext, callback_data: dict, **kwargs):
    markup = await categories_keyboard()
    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text('Что будем проверять?', reply_markup=markup)
    # await callback.message.edit_reply_markup(markup)
    print(f' СБ категорий{callback_data}')

    async with state.proxy() as data:
        if callback_data.get('user') != '0':  # Добавляем юзера в смену
            user: int = int(callback_data.get('user'))
            shift_id: int = data.get('shift_id')
            await update_shift(shift_id, user)

        if callback_data['user'] != '0':
            data['user'] = callback_data['user']
        res = await bool_res(callback_data.get('res'))
        if data.get('question_id') and callback_data.get('question_id') != 'dummy':
            date = datetime.datetime.now()
            await add_result(
                shift_id=data.get('shift_id'),
                user_id=int(data.get('user')),
                date=date,
                category=str(data.get('category')),
                question_id=int(data.get('question_id')),
                result=res
            )


# Функция, которая отдает кнопки с вопросами из категории
async def list_items(callback: CallbackQuery, category, state: FSMContext, callback_data: dict, **kwargs):
    async with state.proxy() as data:
        data['category'] = callback_data['category']
        markup = await questions_keyboard(category)
        # Изменяем сообщение, и отправляем новые кнопки с внутрянкой вопроса (T/F)
        await callback.message.edit_text(text="А конкретнее?", reply_markup=markup)
    print(f' СБ вопросов{callback_data}')


# Функция, которая отдает клавиатуру с результатами T/F
async def show_item(callback: CallbackQuery, category, item_id, state: FSMContext, callback_data: dict, **kwargs):
    markup = item_keyboard(category, item_id)
    question = await get_single_question(int(callback_data.get('question_id')))
    await callback.message.edit_text(question.text, reply_markup=markup)
    print(f' СБ ответов{callback_data}')
    async with state.proxy() as data:
        data['question_id'] = callback_data['question_id']


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter(), state='*')
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """
    current_level = callback_data.get("level")
    category = callback_data.get("category")
    item_id = callback_data.get("item_id")
    cur_state = dp.get_current().current_state()

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_shifts,  # Отдаем смены
        "1": list_categories,  # Отдаем категории
        "2": list_items,  # Отдаем вопросы
        "3": show_item,  # Отдаем ответы
    }
    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]
    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        state=cur_state,
        callback_data=callback_data,
        category=category,
        item_id=item_id
    )


@dp.callback_query_handler(state="*", text='finish_shift')
async def finish_shift(call: CallbackQuery, state: FSMContext):
    cur_shift = await get_cur_shift()
    result = await count_positive_results(cur_shift)
    res_str = str(result)
    prev_score = await count_positive_results_prev_shift()
    async with state.proxy() as data:
        user_id = int(data['user'])
        user_name = await get_user_first_name(user_id)
        if res_str[-1] == '1':
            await call.message.answer(f"{user_name},cпасибо за работу! Вы набрали 🔥{result}🔥 балл за сегодняшнюю смену \n" \
            f"За прошлую смену вы набрали 🔥{prev_score}🔥 положительных результатов.")

        elif result in range(2, 4):
            await call.message.answer(f"{user_name},cпасибо за работу! Вы набрали 🔥{result}🔥 балла за сегодняшнюю смену \n" \
            f"За прошлую смену вы набрали 🔥{prev_score}🔥 положительных результатов.")

        else:
            await call.message.answer(f"{user_name},cпасибо за работу! Вы набрали 🔥{result}🔥 баллов за сегодняшнюю смену \n" \
            f"За прошлую смену вы набрали 🔥{prev_score}🔥 положительных результатов.")

    # await call.message.answer(f"В следующую смену обратите внимание на следующие моменты:{}")

    await state.reset_state()
    await call.message.answer("Чтобы начать новую смену введите команду /menu")


@dp.callback_query_handler(state="*", text='add_user')
async def finish_shift(call: CallbackQuery):
    await call.message.answer("Пожалуйста представьтесь. Имя и Фамилия в одну строчку через пробел")
    await States.add_user.set()


@dp.message_handler(state=States.add_user)
async def add_new_user(message: Message):
    name = message.text
    f_name, s_name = name.split(' ')
    if f_name.isdigit() or s_name.isdigit():
        await message.answer("Некорректное имя.Попробуйте заново")
        return
    print(name)

    if not await user_exist(name):
        await add_user(name=name)
        await message.answer("Пользователь добавлен.Чтобы начать новую смену введите команду /menu")
    else:
        await message.answer("Пользователь c таким именем уже существует. Введите другое имя или внимательно "
                             "приглядитесь к существующему списку")
        return
