from aiogram.types import Message

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


async def answer_thread(user, bot, flood_exp_answers):
    await bot.send_message(conf.admin.supergroup_id, await formate_flood_app(flood_exp_answers), user.thread_id)


async def formate_flood_app(flood_exp_answers):
    report = ''
    for step, question in enumerate(QUESTIONS_DETAILS):
        report = report + f'<strong>{QUESTIONS_DETAILS[step].text}</strong> - {flood_exp_answers.details[step]}\n\n'
    for step, question in enumerate(QUESTIONS_FORM):
        report = report + f'<b>{QUESTIONS_FORM[step].text}</b> - {flood_exp_answers.form[step]}\n\n'

    for step, question in enumerate(QUESTIONS_DOCUMENTS):
        report = report + f'{QUESTIONS_DOCUMENTS[step].text} - {flood_exp_answers.documents[step]}\n\n'

    return report


