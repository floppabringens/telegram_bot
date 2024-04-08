from .inline import get_callback_btns
from .reply import get_keyboard
from aiogram.types import KeyboardButton
from .text_builder import MENU_WITH_APPS_KB, MENU_NO_APPS_KB, MENU_WITH_MODERATED_APPS_KB

async def check_status(apps):
    for app in apps:
        if app.status in (1,2):
            return True

async def MENU_KB(user):
    if not user.flood_applications:
        return MENU_NO_APPS_KB
    elif await check_status(user.flood_applications):
        return MENU_WITH_MODERATED_APPS_KB
    else:
        return MENU_WITH_APPS_KB
