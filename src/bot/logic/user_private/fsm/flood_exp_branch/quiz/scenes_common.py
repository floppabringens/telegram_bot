from dataclasses import dataclass

from aiogram import F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import Message

from src.bot.kbds.text_builder import BUTTON_CANCEL, BUTTON_BACK


@dataclass
class FloodExpAnswers:
    details: list[str] | None = None
    form: list[str] | None = None
    documents: list[str] | None = None


flood_exp_answers = FloodExpAnswers()

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
        text='Ваш номер телефона',
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
]


QUESTIONS_DOCUMENTS = [
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

