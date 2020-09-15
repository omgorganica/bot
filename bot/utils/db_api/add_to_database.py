import datetime
from typing import Any, Union

from utils.db_api.db_commands import add_user, add_question, add_result, count_done_in_cat, get_cur_shift, check_done, \
    get_user_first_name, update_shift
import emoji
import asyncio
from utils.db_api.database import create_db

technic_and_territory = emoji.emojize(':rocket:') + 'Техника и территория'
staff = emoji.emojize(':man:') + 'Персонал'
procedures = emoji.emojize(':bar_chart:') + 'Процедуры'


# Используем эту функцию, чтобы заполнить базу данных товарами
async def add_items():
    leaders = ['Дмитрий Кучма', 'Семён Руденко', 'Константин Плюхин', 'Владимир Шильков']
    for leader in leaders:
        await add_user(name=leader)

    questions = {
        'Техническое состояние складского оборудования': technic_and_territory,
        'Техническое состояние погрузочной техники': technic_and_territory,
        'Состояние проездов и пешеходных дорожек': technic_and_territory,
        'Состояние балок и стоек в МА': technic_and_territory,
        'Расстановка продукции в МА': technic_and_territory,
        'Наличие у персонала СИЗ и их состояние': staff,
        'Проверка рабочих мест( 5S)': staff,
        'Прохождение инструктажей и наличие допуска к работе': staff,
        'Прохождение медосмотра': staff,
        'Сдача безопасных ножей': staff,
        'Сдача ключей в офис': staff,
        'Проверка аптечки': staff,
        'Снятие остатков': procedures,
        'Проверка сборных паллет ': procedures,
        'Контроль сбора брака': procedures,
        'Контроль заполнения листа отгрузки': procedures,
        'Контроль сбора и уборки мусора': procedures,
        'Контроль прессования пленки, картона': procedures,
        'Контроль заполнения листа выгрузки': procedures,
        'Контроль заполнения чек-листа восстановления продукции': procedures,
        'Контроль за работой подрядных организаций': procedures,
    }
    for _question, _category in questions.items():
        await add_question(
            text=_question, category=_category
        )


async def test():
    await update_shift(
        124, 79
    )
loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_items())
# loop.run_until_complete(test())
