from pprint import pprint
from typing import List
from sqlalchemy import and_, exists, update
from utils.db_api.database import db
from utils.db_api.models import ShiftUser, Question, Result, Shift


# Функция для создания нового пользователя. Принимает все возможные аргументы, прописанные в Shift
async def add_user(**kwargs):
    new_item = await ShiftUser(**kwargs).create()
    return new_item


# Функция для создания нового вопроса. Принимает все возможные аргументы, прописанные в Shift
async def add_question(**kwargs):
    new_item = await Question(**kwargs).create()
    return new_item


# Считаем количество элеметнтов

async def count_items(category_item=None, questions=None):
    # Прописываем условия для вывода (категория товара равняется выбранной категории)
    conditions = [Question.category == category_item]

    # Если передали подкатегорию, то добавляем ее в условие
    if category_item:
        conditions.append(Question.category == category_item)

    # Функция подсчета товаров с указанными условиями
    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total


# Функция для вывода пользователей
async def get_users() -> List[ShiftUser]:
    return await ShiftUser.query.distinct(ShiftUser.name).gino.all()


# Функция для вывода списка категорий
async def get_categories() -> List[Question]:
    return await Question.query.distinct(Question.category).gino.all()


# Функция вывода вопросов, состоящих в выбранной категории
async def get_questions(category) -> List[Question]:
    items = await Question.query.where(Question.category == category).gino.all()
    return items


async def add_result(**kwargs):
    new_result = await Result(**kwargs).create()
    return new_result


async def get_cur_shift():
    shift = await Shift.query.gino.all()
    try:
        cur_shift = shift[-1].id
    except IndexError:
        cur_shift = shift[0].id
    return cur_shift


async def add_shift(**kwargs):
    new_shift = await Shift(**kwargs).create()
    return new_shift


async def check_done(shift_id, question_id):
    result = await db.select([db.func.count()]).where(
        and_(Result.shift_id == shift_id, Result.question_id == question_id)
    ).gino.scalar()
    if result >= 1:
        return True
    else:
        return False


async def count_done_in_cat(shift_id, category):
    total = await db.select([db.func.count()]).where(
        and_(Result.shift_id == shift_id, Result.category == category)
    ).gino.scalar()
    return total


async def count_positive_results(shift_id):
    total = await db.select([db.func.count()]).where(
        and_(Result.shift_id == shift_id, Result.result == True)
    ).gino.scalar()
    shift = await Shift.get(shift_id)
    await shift.update(score=total).apply()
    return total

async def count_positive_results_prev_shift(user_id):
    shifts = await Shift.query.where(Shift.user_id == user_id).gino.all()
    prev_score = shifts[-2].score
    return prev_score


async def get_negative_results(shift_id):
    items = await db.select().where(
        and_(Result.shift_id == shift_id, Result.result == False)
    ).gino.all()
    return items


async def get_single_question(id):
    item = await Question.query.where(Question.id == id).gino.first()
    return item


async def get_user_first_name(user):
    item = await ShiftUser.query.where(ShiftUser.id == user).gino.first()
    full_name = item.name
    f_name, l_name = full_name.split(' ')
    return f_name


async def user_exist(user):
    total = await db.select([db.func.count()]).where(
        and_(ShiftUser.name == user)
    ).gino.scalar()
    if total >= 1:
        return True
    else:
        return False


async def update_shift(shift_id, user_id):
    shift = await Shift.get(shift_id)
    await shift.update(user_id=user_id).apply()

