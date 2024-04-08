
from aiogram import Router, types, F
from aiogram.filters import Command, or_f

from src.bot.filters.chat_types import ChatTypeFilter

from aiogram.fsm.context import FSMContext

from src.bot.kbds.app_deletion_menu_logic import DELETION_MENU, CONFIRMATION_DELETION_MENU
from src.bot.kbds.main_menu_logic import MENU_KB
from src.bot.kbds.text_builder import BUTTON_MENU
from src.bot.structures.status import Status
from src.configuration import conf

my_applications_router = Router(name='my_applications')
my_applications_router.message.filter(ChatTypeFilter(["private"]))

@my_applications_router.message(F.text.lower() == 'мои заявки')
async def my_apps_handler(message: types.Message, state: FSMContext, db,):
    """Menu command handler."""
    await state.clear()

    await message.answer('Ваши заявки:',
                         reply_markup=BUTTON_MENU
                         )

    user = await db.user.get(message.from_user.id)

    for app in user.flood_applications:
        if app.is_deleted is False:
            if app.status == 0:
                status = '<strong>Заявка еще не промодерирована</strong>'
            elif app.status == 1:
                status = '<strong>Заявка принята</strong>'
            elif app.status == 2:
                status = '<strong>Заявка отклонена</strong>'
            else:
                status = '<strong>Работа по заявке завершена</strong>'
            await message.answer_document(document=app.pdf_id, caption=f'{status}', reply_markup=await DELETION_MENU(app.id))



@my_applications_router.callback_query(F.data.startswith('delete_'))
async def start_handler(callback: types.CallbackQuery, state: FSMContext, db):

    id = int(callback.data.split('_')[-1])

    await callback.answer('Вы уверены?')
    await callback.message.edit_reply_markup(reply_markup=await CONFIRMATION_DELETION_MENU(id))


@my_applications_router.callback_query(F.data.startswith('deletion_confirm_'))
async def start_handler(callback: types.CallbackQuery, state: FSMContext, db, bot):

    id = int(callback.data.split('_')[-1])

    flood_app = await db.flood_application.get(id)

    await bot.edit_message_caption(conf.admin.supergroup_id, flood_app.moder_message_id,
                                   caption= f'<strong>❌ Заявка <code>{id}</code> удалена пользователем</strong>')

    if flood_app.status == 0:
        await db.flood_application.delete(flood_app.id)
    else:
        await db.flood_application.update_is_deleted(flood_app.id, True)
    await db.session.commit()

    await callback.message.edit_caption(caption='Это заявление удалено')
    await callback.answer('Ваше заявление удалено')



@my_applications_router.callback_query(F.data.startswith('deletion_return_'))
async def start_handler(callback: types.CallbackQuery, state: FSMContext, db, ):

    id = int(callback.data.split('_')[-1])

    await callback.message.edit_reply_markup(reply_markup=await DELETION_MENU(id))



