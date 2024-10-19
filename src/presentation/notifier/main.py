import asyncio

from loguru import logger
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from src.infrastructure.cache import redis_client
from src.presentation.bot.bot import bot



async def send_notification(payload: dict) -> None:
    if payload.get("miniapp_btn_url"):
        btn_text = payload.get("miniapp_btn_text") or "👁‍🗨"
        inline_markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=btn_text, web_app=WebAppInfo(url=payload["miniapp_btn_url"]))
            ]
        ])
    else:
        inline_markup = None
    await bot.send_message(payload["user_id"], payload["text"], reply_markup=inline_markup)
    logger.info(f"Sent notification | {payload['user_id']} | {payload['text']}")

async def notifier_worker():
    try:
        await redis_client.connect()
        running = True
        while running:
            await asyncio.sleep(1)
            messages = await redis_client.lpop("send_notification_queue", 20)
            if not messages:
                continue
            logger.info(f"In queue {len(messages)} messages")
            for message in messages:
                try:
                    await send_notification(message)
                except Exception as e:
                    logger.error(e)
    finally:
        await redis_client.close()

if __name__ == "__main__":
    asyncio.run(notifier_worker())
