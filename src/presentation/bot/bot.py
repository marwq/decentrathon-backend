from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from config import settings



bot = Bot(
    settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode="HTML",
    ),
)