from aiogram.filters.callback_data import CallbackData

from .inline import get_callback_btns
from .reply import get_keyboard
from aiogram.types import KeyboardButton

async def DELETION_MENU(id):
    deletion_menu = get_callback_btns(btns={'Удалить':f'delete_{id}'}, sizes=(1,))
    return deletion_menu

async def CONFIRMATION_DELETION_MENU(id):
    confirmation_deletion_menu = get_callback_btns(btns={'Подтвердить':f'deletion_confirm_{id}',
                                           'Вернуться':f'deletion_return_{id}'}, sizes=(2,))
    return confirmation_deletion_menu

