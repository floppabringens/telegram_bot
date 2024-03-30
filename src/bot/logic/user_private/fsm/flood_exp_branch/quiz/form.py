from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import on
from aiogram.types import Message

from src.bot.common.files import files
from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.kbds.reply import get_keyboard
from src.bot.kbds.text_builder import BUTTON_MENU
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.documents import DocumentsQuiz
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.scenes_common import QuestionWithType, CancellableScene, \
    flood_exp_answers, QUESTIONS_FORM


class FormQuiz(CancellableScene, state="form"):

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None = 0) -> Any:

        if not step:
            await message.answer(
                'Для проведения эĸспертизы вам нужно заполнить заявление форме и приĸрепить необходимые доĸументы.'
                'Ниже прикреплена форма с пустыми полями. Ознакомьтесь с шаблоном, а далее последовательно'
                'отвечайте на вопросы бота.')

            await message.answer_document(files['form_template'])
            # This is the first step, so we should greet the user
        try:
            QUESTIONS_FORM[step]
        except IndexError:
            # This error means that the question's list is over
            await self.on_succ_leave_from_form(message, state)
            return await self.wizard.goto(DocumentsQuiz)

        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS_FORM[step].text,
            reply_markup=get_keyboard("🔙 Назад",
                                      "❌ Выход"
                                      )
        )

    async def on_succ_leave_from_form(self, message: Message, state: FSMContext):

        data = await state.get_data()

        answers = data.get('answers', {})

        user_answers = []

        for step, question in enumerate(QUESTIONS_FORM):
            answer = answers.get(step)
            user_answers.append(f'{answer}')

        flood_exp_answers.form = user_answers

        await state.set_data({})


    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:

        await message.answer('Что вас интересует?.',
                             reply_markup=BUTTON_MENU
                             )

        await state.set_data({})

    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:

        data = await state.get_data()
        step = data["step"]
        answers = data.get("answers", {})

        print(message.content_type)

        if step == 1:
            await message.answer("Давайте заполним адрес квартиры.")

        answers[step] = message.text

        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

    @on.message()
    async def unknown_message(self, message: Message) -> None:

        await message.answer('Пожалуйста, отправьте текст.')
