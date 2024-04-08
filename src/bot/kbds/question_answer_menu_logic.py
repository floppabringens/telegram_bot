from aiogram.filters.callback_data import CallbackData

from .inline import get_callback_btns
from .reply import get_keyboard
from aiogram.types import KeyboardButton


async def BUTTON_ANSWER_QUESTION(id):

    button_answer_question = get_callback_btns(btns={'Ответить на вопрос': f'answer_question_{id}'}, sizes=(1,))

    return button_answer_question

async def RETURN_QUESTION_MENU(id):
    return_question_menu = get_callback_btns(btns={'Вернуться': f'return_{id}', 'Отправить ответ': f'send_{id}'}, sizes=(2,))
    return return_question_menu
