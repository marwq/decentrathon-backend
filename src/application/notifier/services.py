from src.infrastructure.cache import redis_client


async def send_notification_to_queue(
    user_id: int, 
    text: str, 
    miniapp_btn_url: str | None = None,
    miniapp_btn_text: str | None = None,
) -> None:
    payload = dict(
        user_id=user_id,
        text=text,
        miniapp_btn_url=miniapp_btn_url,
        miniapp_btn_text=miniapp_btn_text,
    )
    await redis_client.rpush("send_notification_queue", payload)

