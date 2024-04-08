from aiogram.filters.callback_data import CallbackData

from .inline import get_callback_btns
from .reply import get_keyboard
from aiogram.types import KeyboardButton

MENU_NO_APPS_KB = get_keyboard(
    'Экспертиза по затоплению',
    'Экспертиза другого вида',
    'Вопрос',
    placeholder='Что вас интересует?',
    sizes=(1, 1, 1))

MENU_WITH_APPS_KB = get_keyboard(
    'Экспертиза по затоплению',
    'Экспертиза другого вида',
    'Вопрос',
    'Мои заявки',
    placeholder='Что вас интересует?',
    sizes=(1, 1, 2))

MENU_WITH_MODERATED_APPS_KB = get_keyboard(
    'Экспертиза по затоплению',
    'Экспертиза другого вида',
    'Вопрос',
    'Мои заявки',
    'Чат с экспертом',
    placeholder='Что вас интересует?',
    sizes=(1, 1, 2, 1))


BUTTON_MENU = get_keyboard(
    'Меню',
    placeholder='Вернуться в меню?',
    sizes=(1,)
)

BUTTON_CONTINUE = get_keyboard(
    'Продолжить',
    placeholder='Продолжить?',
    sizes=(1,)
)


BUTTON_AGREE = get_keyboard(
    'Не имею ничего против',
    placeholder='Согласны?',
    sizes=(1,)
)


BUTTON_CANCEL = KeyboardButton(text='❌ Выход')
BUTTON_BACK = KeyboardButton(text='🔙 Назад')

BUTTON_CHAT_EXIT = get_callback_btns(btns={'Выйти из чата':'exit_chat'}, sizes=(1,))

MENU_CHAT = get_callback_btns(btns={'Отправить':'send_chat', 'Выйти из чата':'exit_chat'}, sizes=(2,))


