from aiogram.filters.callback_data import CallbackData

from .inline import get_callback_btns
from .reply import get_keyboard
from aiogram.types import KeyboardButton

async def MODERATION_MENU(id):
    moderation_menu = get_callback_btns(btns={'Принять': f'accept_{id}', 'Отклонить': f'decline_{id}'}, sizes=(2,))
    return moderation_menu

async def CONFIRMATION_DEC_MENU(id):
    confirmation_dec_menu = get_callback_btns(btns={'Подтвердить':f'dec_confirm_{id}',
                                           'Вернуться':f'return_{id}'}, sizes=(2,))
    return confirmation_dec_menu

async def CONFIRMATION_ACC_MENU(id):
    confirmation_acc_menu = get_callback_btns(btns={'Подтвердить':f'acc_confirm_{id}',
                                           'Вернуться':f'return_{id}'}, sizes=(2,))
    return confirmation_acc_menu

