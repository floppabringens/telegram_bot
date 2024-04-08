from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from src.bot.kbds.app_moderation_menu_logic import MODERATION_MENU
from src.bot.kbds.question_answer_menu_logic import BUTTON_ANSWER_QUESTION
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.scenes_common import QUESTIONS_DETAILS, QUESTIONS_FORM, \
    QUESTIONS_DOCUMENTS

from src.configuration import conf


async def create_thread(user, db, bot):

    if not await db.user.is_thread_exists(user.user_id):
        name = f'Клиент #{user.user_id}'
        thread_data = await bot.create_forum_topic(chat_id=conf.admin.supergroup_id, name=name)
        await db.user.update_thread(user.user_id, thread_data.message_thread_id)
        await db.session.commit()
    else:
        try:
            message = await bot.send_message(conf.admin.supergroup_id, '.', user.thread_id)
            await message.delete()

        except TelegramBadRequest:
            name = f'Клиент #{user.user_id}'
            thread_data = await bot.create_forum_topic(chat_id=conf.admin.supergroup_id, name=name)
            await db.user.update_thread(user.user_id, thread_data.message_thread_id)
            await db.session.commit()





async def answer_thread(user, bot, text: str):
    await bot.send_message(conf.admin.supergroup_id, text, user.thread_id)


async def remove_first_word(input_string):
    # Разбиваем строку на слова по пробелам
    words = input_string.split()

    # Удаляем первое слово
    if len(words) > 1:
        # Если в строке есть хотя бы два слова, удаляем первое слово
        result_string = ' '.join(words[1:])
    else:
        # Если в строке только одно слово, возвращаем пустую строку
        result_string = ''

    return result_string

async def send_flood_app(user, flood_exp_answers, db, bot):

    report = f'<strong>📩🚣🏼‍ | Новая заявка на проведение экспертизы по затоплению от пользователя с id <code>{user.user_id}</code></strong>\n\n\n'

    for step, _ in enumerate(QUESTIONS_DETAILS):
        report = report + f'<strong>{QUESTIONS_DETAILS[step].text}</strong>  -  {flood_exp_answers.details[step]}\n\n'

    report = report + '\n\n'

    for step, _ in enumerate(QUESTIONS_FORM):
        report = report + f'<b>{QUESTIONS_FORM[step].text}</b>  -  <code>{flood_exp_answers.form[step]}</code>\n\n'
    await bot.send_message(conf.admin.supergroup_id, report, user.thread_id)

    media_group = MediaGroupBuilder()

    for step, _ in enumerate(QUESTIONS_DOCUMENTS):
        media_group.add_document(flood_exp_answers.documents[step], caption = await remove_first_word(QUESTIONS_DOCUMENTS[step].text))

    await bot.send_media_group(chat_id=conf.admin.supergroup_id, media=media_group.build(),
                               message_thread_id=user.thread_id)


    message = await bot.send_document(chat_id=conf.admin.supergroup_id, caption=f'<strong>Модерация заявки <code>{user.flood_applications[-1].id}</code></strong>',
                            document=user.flood_applications[-1].pdf_id, message_thread_id=user.thread_id, reply_markup=await MODERATION_MENU(user.flood_applications[-1].id))

    print(message.message_id)
    await db.flood_application.update_moder_message_id(user.flood_applications[-1].id, message.message_id)
    await db.session.commit()




async def send_all_flood_apps(user, bot):
    for flood_app in user.flood_applications.scalars():
        report = ''
        for step, _ in enumerate(QUESTIONS_DETAILS):
            report = report + f'<strong>{QUESTIONS_DETAILS[step].text}</strong> - <i>{flood_app.details[step]}</i>\n\n'
        for step, _ in enumerate(QUESTIONS_FORM):
            report = report + f'<b>{QUESTIONS_FORM[step].text}</b> - <i>{flood_app.form[step]}</i>\n\n'
        await bot.send_message(conf.admin.supergroup_id, report)

        media_group = MediaGroupBuilder()

        for step, _ in enumerate(QUESTIONS_DOCUMENTS):
            media_group.add_document(flood_app.documents[step],
                                     caption=await remove_first_word(QUESTIONS_DOCUMENTS[step].text))

        await bot.send_media_group(chat_id=conf.admin.supergroup_id, media=media_group.build(),
                                   )



async def send_question(user, question_text, bot):
    report = (f'<strong>📩❓ | Новый вопрос от пользователя с id <code>{user.user_id}</code></strong>\n\n'
              f'<strong>Текст вопроса:</strong>\n{question_text}')

    id = user.questions[-1].id

    await bot.send_message(conf.admin.supergroup_id, report, user.thread_id,
                           reply_markup=await BUTTON_ANSWER_QUESTION(id))
