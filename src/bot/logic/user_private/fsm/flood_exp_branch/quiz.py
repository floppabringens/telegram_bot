from dataclasses import dataclass
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, SceneRegistry, on
from aiogram.types import KeyboardButton, Message, ContentType

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.bot.logic.user_private.fsm.flood_exp_branch.flood_exp import FloodExp
from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.kbds.reply import get_keyboard
from src.bot.kbds.text_builder import BUTTON_CANCEL, BUTTON_BACK, BUTTON_MENU
from src.bot.common.files import files

quiz_router = Router()
quiz_router.message.filter(ChatTypeFilter(["private"]))

@dataclass
class Answer:
    """
    Represents an answer to a question.
    """

    text: str
    """The answer text"""
    # is_correct: bool = False
    """Indicates if the answer is correct"""


@dataclass
class QuestionWithAnswer:
    """
    Class representing a quiz with a question and a list of answers.
    """

    text: str
    """The question text"""
    answers: list[Answer]
    """List of answers"""


@dataclass
class QuestionWithType:
    """
    Class representing a quiz with a question and a list of answers.
    """

    text: str
    """The question text"""
    type: Message.content_type
    """Expecting type"""


# Fake data, in real application you should use a database or something else
QUESTIONS_DETAILS = [
    QuestionWithAnswer(
        text='Кто вы?',
        answers=[
            Answer(text='Гражданин'),
            Answer(text='Юридическое лицо')
        ]
    ),
    QuestionWithAnswer(
        text='Ваш регион.',
        answers=[
            Answer(text='Харьковская область'),
            Answer(text='Другой')
        ]
    ),
    QuestionWithAnswer(
        text='Общая площадь квартиры.',
        answers=[
            Answer(text='до 40 кв.м'),
            Answer(text='от 40 до 80 кв.м'),
            Answer(text='от 80 кв.м')
        ]
    ),
    QuestionWithAnswer(
        text='Наличие поврежденной мебели.',
        answers=[
            Answer(text='да'),
            Answer(text='нет'),
        ]
    ),
    QuestionWithAnswer(
        text='Наличие поврежденной электротехники.',
        answers=[
            Answer(text='да'),
            Answer(text='нет'),
        ]
    ),
]

QUESTIONS_FORM = [
    QuestionWithType(
        text='Ваше Ф.И.О',
        type=ContentType.TEXT
    ),
    QuestionWithType(
        text='Вам номер телефона',
        type=ContentType.TEXT
    ),
    QuestionWithType(
        text='Улица',
        type=ContentType.TEXT
    ),
    QuestionWithType(
        text='Номер дома',
        type=ContentType.TEXT
    ),
    QuestionWithType(
        text='Номер квартиры',
        type=ContentType.TEXT
    ),
    QuestionWithType(
        text='Дата затопления',
        type=ContentType.TEXT
    ),
    QuestionWithType(
        text='Отправьте документ акта про затопление',
        type=ContentType.DOCUMENT
    ),
    QuestionWithType(
        text='Отправьте договор купле-продажи',
        type=ContentType.DOCUMENT
    ),
    QuestionWithType(
        text='Отправьте технический паспорт на квартиру',
        type=ContentType.DOCUMENT
    ),
    QuestionWithType(
        text='Отправьте акт про последствия затопления',
        type=ContentType.DOCUMENT
    ),
    # QuestionWithType(
    #     text='Отправьте другие документы на ваше усмотрение',
    #     type=ContentType.DOCUMENT
    # ),
]


class Flood_Exp_Answers:
    quiz: list[str]
    form: list[str]
# {"quiz": [], "form": []}

class CancellableScene(Scene):

    @on.message(F.text.casefold() == BUTTON_CANCEL.text.casefold())
    async def handle_cancel(self, message: Message) -> None:
        # await message.answer("Cancelled.", reply_markup=ReplyKeyboardRemove())
        await self.wizard.exit()

    @on.message(F.text.casefold() == BUTTON_BACK.text.casefold())
    async def handle_back(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        step = data['step']

        previous_step = step - 1
        if previous_step < 0:
            # In case when the user tries to go back from the first question,
            # we just exit the quiz
            return await self.wizard.exit()
        return await self.wizard.back(step=previous_step)


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
            await self.on_succ_leave(message, state)
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

    async def on_succ_leave(self, message: Message, state: FSMContext):

        data = await state.get_data()

        answers = data.get('answers', {})

        user_answers = []

        for step, question in enumerate(QUESTIONS_DETAILS):
            answer = answers.get(step)
            user_answers.append(f'{answer}')

        Flood_Exp_Answers.quiz = user_answers

        await state.set_data({})

        await message.answer(
            'Для проведения эĸспертизы вам нужно заполнить заявление форме и приĸрепить необходимые доĸументы.'
            'Ниже прикреплена форма с пустыми полями. Ознакомьтесь с шаблоном, а далее последовательно'
            'отвечайте на вопросы бота.')

        await message.answer_document(files['form_template'])

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


class FormQuiz(CancellableScene, state="form"):

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None = 0) -> Any:


        if not step:
            # This is the first step, so we should greet the user
            await message.answer("Заполните заявление по форме")

        try:
            QUESTIONS_FORM[step]
        except IndexError:
            # This error means that the question's list is over
            return await self.wizard.exit()

        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS_FORM[step].text,
            reply_markup=get_keyboard("🔙 Назад",
                                      "❌ Выход"
                                      )
        )

    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext, db) -> None:

        data = await state.get_data()

        answers = data.get("answers", {})

        user_answers = []

        for step, question in enumerate(QUESTIONS_FORM):
            answer = answers.get(step)
            user_answers.append(f"{answer}")

        try:
            last = user_answers[9]

            Flood_Exp_Answers.form = user_answers

            user = await db.user.get(message.from_user.id)
            await db.flood_application.new(user=user, quiz=Flood_Exp_Answers.quiz,
                                           form=Flood_Exp_Answers.form)
            await db.session.commit()

            await message.answer(
                "Ваше заявление принято, в ближайшее время специалист его проверит."
                " А таĸже вы можете проверить статус модерации в меню.",
                reply_markup=BUTTON_MENU
            )
        except IndexError:
            await message.answer(
                "Что вас интересует?",
                reply_markup=BUTTON_MENU
            )

        await state.set_data({})

    @on.message()
    async def answer(self, message: Message, state: FSMContext) -> None:

        data = await state.get_data()
        step = data["step"]
        answers = data.get("answers", {})
        # answers[step] = message.photo

        print(message.content_type)

        for i in range(0, 9):
            if step == i and message.content_type is not QUESTIONS_FORM[i].type:
                await message.answer("Пожалуйста, отправьте текст")
                return

        if step == 1:
            await message.answer("Давайте заполним адрес квартиры.")

        if step == 5:
            await message.answer("Перейдем к документам! Далее прикрепляйте файлы поддерживаемых форматов: PDF, DOC, DOCX")

        if step in range(0, 5):
            answers[step] = message.text
        else:
            answers[step] = message.document.file_id
        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

    @on.message()
    async def unknown_message(self, message: Message) -> None:

        await message.answer('Пожалуйста, отправьте корректные данные.')


# Add handler that initializes the scene
quiz_router.message.register(DetailsQuiz.as_handler(), FloodExp.application_on_flood, F.text.casefold() == "продолжить")

scene_registry = SceneRegistry(quiz_router)
scene_registry.add(DetailsQuiz, FormQuiz)
