from typing import Any

from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import on
from aiogram.types import Message

from src.bot.kbds.reply import get_keyboard
from src.bot.kbds.text_builder import BUTTON_MENU
from src.bot.logic.moder_supergroup.thread_work import create_thread, answer_thread, send_flood_app
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.scenes_common import QuestionWithType, CancellableScene, \
    flood_exp_answers, QUESTIONS_DOCUMENTS, QUESTIONS_DETAILS
from src.bot.pdf.pdf_creation import send_pdf


class DocumentsQuiz(CancellableScene, state="documents"):

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None = 0) -> Any:

        if not step:
            await message.answer('Перейдем к документам! '
                                 'Далее прикрепляйте файлы поддерживаемых форматов: PDF, DOC, DOCX.'
                                 )

        try:
            quiz = QUESTIONS_DOCUMENTS[step]
        except IndexError:
            # This error means that the question's list is over
            return await self.wizard.exit()

        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS_DOCUMENTS[step].text,
            reply_markup=get_keyboard("🔙 Назад",
                                      "❌ Выход"
                                      )
        )

    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext, db, bot) -> None:

        data = await state.get_data()

        answers = data.get("answers", {})

        user_answers = []

        for step, question in enumerate(QUESTIONS_DOCUMENTS):
            answer = answers.get(step)
            user_answers.append(f"{answer}")

        try:
            last = user_answers[3]

            flood_exp_answers.documents = user_answers

            user = await db.user.get(message.from_user.id)

            await db.user.update_real_name(user.user_id, flood_exp_answers.form[0])

            await create_thread(user, db, bot)

            user = await db.user.get(message.from_user.id)

            flood = await send_pdf(user, flood_exp_answers, bot)

            pdf_id = flood.document.file_id

            user_message_id = flood.message_id

            if flood_exp_answers.details[2] == QUESTIONS_DETAILS[2].answers[0].text:
                price = 100
            elif flood_exp_answers.details[2] == QUESTIONS_DETAILS[2].answers[1].text:
                price = 200
            elif flood_exp_answers.details[2] == QUESTIONS_DETAILS[2].answers[2].text:
                price = 300
            else:
                price = 0

            await db.flood_application.new(user=user, details=flood_exp_answers.details,
                                           form=flood_exp_answers.form, documents=flood_exp_answers.documents, pdf_id=pdf_id,
                                           user_message_id=user_message_id, price=price)

            await db.session.commit()

            user = await db.user.get(message.from_user.id)

            await send_flood_app(user, flood_exp_answers, db, bot)



        except IndexError:
            await message.answer(
                "Что вас интересует?",
                reply_markup=BUTTON_MENU
            )

        await state.set_data({})

    @on.message(F.document)
    async def answer(self, message: Message, state: FSMContext) -> None:

        data = await state.get_data()
        step = data["step"]
        answers = data.get("answers", {})

        print(message.content_type)

        answers[step] = message.document.file_id

        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

    @on.message()
    async def unknown_message(self, message: Message) -> None:

        await message.answer('Пожалуйста, отправьте документ.')
