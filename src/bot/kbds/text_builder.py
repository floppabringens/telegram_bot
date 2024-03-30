from .inline import get_callback_btns
from .reply import get_keyboard
from aiogram.types import KeyboardButton

MENU_KB = get_keyboard(
    'Экспертиза по затоплению',
    'Экспертиза другого вида',
    'Вопрос',
    placeholder='Что вас интересует?',
    sizes=(1, 1, 1)
)

MENU_KB_ = get_keyboard(
    'Экспертиза по затоплению',
    'Экспертиза другого вида',
    'Вопрос',
    'Мои заявки',
    'Перейти в чат с экспертом',
    placeholder='Что вас интересует?',
    sizes=(1, 2, 1)
)


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