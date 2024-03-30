
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.scenes_common import QUESTIONS_DETAILS, QUESTIONS_FORM, \
    QUESTIONS_DOCUMENTS

from src.configuration import conf


async def create_thread(user, db, bot, flood_exp_answers):
    if not await db.user.is_thread_exists(user.user_id):
        if str(flood_exp_answers.details[0]) == 'Юридическое лицо':
            name = f'#{user.user_id} | Юридическое лицо'
        else:
            name = f'#{user.user_id} | {user.user_real_name}'
        thread_data = await bot.create_forum_topic(chat_id=conf.admin.supergroup_id, name=name)
        print(str(thread_data.message_thread_id))
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

async def send_flood_app(bot, user, id: int | None = -1):
    report = ''
    flood_app = user.flood_applications[id]
    for step, _ in enumerate(QUESTIONS_DETAILS):
        report = report + f'<strong>❓️  {QUESTIONS_DETAILS[step].text}</strong>  ➡️  <i>{flood_app.details[step]}</i>  ✅\n\n'
    for step, _ in enumerate(QUESTIONS_FORM):
        report = report + f'<b>❓️  {QUESTIONS_FORM[step].text}</b>  ➡️  <i>{flood_app.form[step]}</i>  ✅\n\n'
    await bot.send_message(conf.admin.supergroup_id, report, user.thread_id)

    media_group = MediaGroupBuilder()



    for step, _ in enumerate(QUESTIONS_DOCUMENTS):
        media_group.add_document(flood_app.documents[step], caption = await remove_first_word(QUESTIONS_DOCUMENTS[step].text))

    await bot.send_media_group(chat_id=conf.admin.supergroup_id, media=media_group.build(),
                               message_thread_id=user.thread_id7
                               )

    async def send_user_flood_app(bot, user, id: int | None = -1):
        report = ''
        flood_app = user.flood_applications[id]
        for step, _ in enumerate(QUESTIONS_DETAILS):
            report = report + f'<strong>❓️ {QUESTIONS_DETAILS[step].text}</strong> ➡️ <i>{flood_app.details[step]}</i>\n\n'
        for step, _ in enumerate(QUESTIONS_FORM):
            report = report + f'<b>❓️ {QUESTIONS_FORM[step].text}</b> ➡️ <i>{flood_app.form[step]}</i>\n\n'
        await bot.send_message(conf.admin.supergroup_id, report)

        media_group = MediaGroupBuilder()

        for step, _ in enumerate(QUESTIONS_DOCUMENTS):
            media_group.add_document(flood_app.documents[step],
                                     caption=await remove_first_word(QUESTIONS_DOCUMENTS[step].text))

        await bot.send_media_group(chat_id=conf.admin.supergroup_id, media=media_group.build(),
                                   )


    # for step, _ in enumerate(QUESTIONS_DOCUMENTS):
    #     print(flood_app.documents[step]+'\n')
    #     await bot.send_document(conf.admin.supergroup_id, flood_app.documents[step],
    #                             user.thread_id, caption=remove_first_word(QUESTIONS_DOCUMENTS[step].text)
    #                             )




async def formate_flood_app(flood_exp_answers):
    report = ''
    for step, question in enumerate(QUESTIONS_DETAILS):
        report = report + f'<strong>{QUESTIONS_DETAILS[step].text}</strong> - {flood_exp_answers.details[step]}\n\n'
    for step, question in enumerate(QUESTIONS_FORM):
        report = report + f'<b>{QUESTIONS_FORM[step].text}</b> - {flood_exp_answers.form[step]}\n\n'

    for step, question in enumerate(QUESTIONS_DOCUMENTS):
        report = report + f'{QUESTIONS_DOCUMENTS[step].text} - {flood_exp_answers.documents[step]}\n\n'

    return report


