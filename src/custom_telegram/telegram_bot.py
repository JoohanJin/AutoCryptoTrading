import telegram
import json
import asyncio
import tracemalloc
import os

def get_credential() -> str:
    """
    get the telegram bot credential stored locally.
    """
    api_key = os.getenv('TELEGRAM_API_KEY')
    channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    if (not api_key or not channel_id):
        f = open('key.json')
        data = json.load(f)
        return data['api_key'], data['channel_id']
    return api_key, channel_id

async def send_message(bot: telegram.Bot, channel_id: str, message: str) -> None:
    await bot.send_message(
        chat_id = channel_id,
        text = message,
    )
    return

async def send_update()-> None:
    await telegram.pdate.message.reply_text('Hi!')

async def main() -> None:
    api_key, channel_id = get_credential()
    
    bot = telegram.Bot(api_key)

    async with bot:
        await send_message(bot, channel_id, 'Test Message 1, 2, 3')
    return

if (__name__ == "__main__"):
    asyncio.run(main())