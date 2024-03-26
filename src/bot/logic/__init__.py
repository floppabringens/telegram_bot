"""This package is used for a bot logic implementation."""
from src.bot.logic.user_private.menu import menu_router
from src.bot.logic.user_private.start import start_router
from src.bot.logic.admin_private.update_role import admin_router
from src.bot.logic.moderator_private.moderator import moder_router

from src.bot.logic.user_private.fsm.question_branch.question import question_router
from src.bot.logic.user_private.fsm.other_exp_branch.other_exp import other_exp_router
from src.bot.logic.user_private.fsm.flood_exp_branch.flood_exp import flood_exp_router
from src.bot.logic.user_private.fsm.flood_exp_branch.quiz import quiz_router
from src.bot.logic.moder_supergroup.topic import supergroup_router

routers = (start_router, menu_router,
           admin_router, moder_router,
           quiz_router, flood_exp_router,
           question_router, other_exp_router, supergroup_router)
