"""This file represents an echo logic."""

from aiogram import Router, types

from src.bot.filters.chat_types import ChatTypeFilter

echo_router = Router(name='echo')
echo_router.message.filter(ChatTypeFilter(["private"]))


@echo_router.message()
async def start_handler(message: types.Message):
    """Echo handler."""
    await message.answer('Я вас не понимаю. Используйте команду /menu.')
