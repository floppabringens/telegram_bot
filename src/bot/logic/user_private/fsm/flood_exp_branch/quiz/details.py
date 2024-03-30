from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import SceneRegistry, on
from aiogram.types import KeyboardButton, Message

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.bot.logic.user_private.fsm.flood_exp_branch.flood_exp import FloodExp
from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.kbds.text_builder import BUTTON_MENU
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.documents import DocumentsQuiz
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.form import FormQuiz
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.scenes_common import QuestionWithAnswer, Answer, \
    CancellableScene, flood_exp_answers, QUESTIONS_DETAILS

quiz_router = Router()
quiz_router.message.filter(ChatTypeFilter(["private"]))




class DetailsQuiz(CancellableScene, state='details'):

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None = 0) -> Any:

        if not step:
            # This is the first step, so we should greet the user
            await message.answer('Ответьте на вопросы:')

        try:
            quiz = QUESTIONS_DETAILS[step]
        except IndexError:
            # This error means that the question's list is over
            await self.on_succ_leave_from_details(message, state)
            return await self.wizard.goto(FormQuiz)

        markup = ReplyKeyboardBuilder()
        markup.add(*[KeyboardButton(text=answer.text) for answer in quiz.answers])

        if step > 0:
            markup.button(text='🔙 Назад')
        markup.button(text='❌ Выход')

        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS_DETAILS[step].text,
            reply_markup=markup.adjust(2).as_markup(resize_keyboard=True, is_persistent=True),
        )

    async def on_succ_leave_from_details(self, message: Message, state: FSMContext):

        data = await state.get_data()

        answers = data.get('answers', {})

        user_answers = []

        for step, question in enumerate(QUESTIONS_DETAILS):
            answer = answers.get(step)
            user_answers.append(f'{answer}')

        flood_exp_answers.details = user_answers

        await state.set_data({})



    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:

        await message.answer('Что вас интересует?',
                             reply_markup=BUTTON_MENU
                             )

        await state.set_data({})

    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:

        data = await state.get_data()
        step = data["step"]

        answers = data.get("answers", {})

        if step == 0 and message.text.lower() not in [answer.text.lower() for answer in QUESTIONS_DETAILS[0].answers]:
            await message.answer("Выбери корректный вариант!")
            return
        if step == 1 and message.text.lower() not in [answer.text.lower() for answer in QUESTIONS_DETAILS[1].answers]:
            await message.answer("Выбери корректный вариант!")
            return
        if step == 1 and message.text.lower() == "другой":
            await message.answer("Мы поĸа не проводим эĸспертизы в этом регионе")
            return
        if step == 2 and message.text.lower() not in [answer.text.lower() for answer in QUESTIONS_DETAILS[2].answers]:
            await message.answer("Выбери корректный вариант!")
            return
        if step == 3 and message.text.lower() not in [answer.text.lower() for answer in QUESTIONS_DETAILS[3].answers]:
            await message.answer("Выбери корректный вариант!")
            return
        if step == 4 and message.text.lower() not in [answer.text.lower() for answer in QUESTIONS_DETAILS[4].answers]:
            await message.answer("Выбери корректный вариант!")
            return
        if step == 4 and message.text.lower() == "да":
            await message.answer("Мы поĸа не проводим подобный вид эĸспертиз")
            return

        answers[step] = message.text
        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

    @on.message()
    async def unknown_message(self, message: Message) -> None:

        await message.answer("Пожалуйста, выберите ответ.")


# Add handler that initializes the scene
quiz_router.message.register(DetailsQuiz.as_handler(), FloodExp.application_on_flood, F.text.casefold() == "продолжить")

scene_registry = SceneRegistry(quiz_router)
scene_registry.add(DetailsQuiz, FormQuiz, DocumentsQuiz)
