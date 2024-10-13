import telegram
import json
import asyncio
import tracemalloc

def get_credential() -> str:
    """
    get the telegram bot credential stored locally.
    """
    f = open('key.json')
    data = json.load(f)
    return data['api_key'], data['channel_id']

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