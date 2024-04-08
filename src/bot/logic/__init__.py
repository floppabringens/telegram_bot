"""This package is used for a bot logic implementation."""

from src.bot.logic.user_private.menu import menu_router
from src.bot.logic.user_private.my_applications import my_applications_router
from src.bot.logic.user_private.start import start_router
from src.bot.logic.moder_supergroup.update_role import admin_router
from src.bot.logic.moder_supergroup.moderation import moder_router

from src.bot.logic.user_private.fsm.question_branch.question import question_router
# from src.bot.logic.user_private.fsm.other_exp_branch.other_exp import other_exp_router
from src.bot.logic.user_private.fsm.flood_exp_branch.flood_exp import flood_exp_router
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz.details import quiz_router
from src.bot.logic.moder_supergroup.topic import supergroup_router
from src.bot.logic.moder_supergroup.message import message_router
from src.bot.logic.moder_supergroup.answer_question import answer_question_router
from src.bot.logic.moder_supergroup.moder_to_user_chat import moder_to_user_chat_router
from src.bot.logic.user_private.user_to_moder_chat import user_to_moder_chat_router

routers = (start_router, menu_router,
           admin_router, message_router, answer_question_router, moder_to_user_chat_router,
           user_to_moder_chat_router,
           moder_router, my_applications_router,
           quiz_router, flood_exp_router,
           question_router, supergroup_router)
