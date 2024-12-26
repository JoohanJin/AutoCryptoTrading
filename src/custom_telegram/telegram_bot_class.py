from telegram import Bot
import json
import asyncio
from logger.set_logger import log_decorator

class Test:
    def __init__(self) -> None:
        self._telegram_bot = CustomTelegramBot()

    async def testing_message(self) -> str:
        print("Sending the request to send a messge \"Testing\"") # Doing Some Synchronous Task

        await self._telegram_bot.send_text("test messaging")

        return "Testing"

class CustomTelegramBot:
    def __init__(self) -> None:
        # Get the credential from the json
        # will be considered as private attributes.
        self.__api_key, self.__channel_id = self.__get_credential()

        # make the bot instance
        self._bot = Bot(self.__api_key)

        return

    def __get_credential(self) -> str:
        # funcion called when TelegramBot is initialized.
        f = open('./custom_telegram/key.json')
        data = json.load(f)
        return data['api_key'], data['channel_id']

    async def send_text(self, message: str) -> None:
        await self._bot.send_message(
            chat_id = self.__channel_id,
            text = message,
        )
        return

"""
############################################################################################
#                                     Running Code Zone                                    #
############################################################################################
"""

async def main():
    test = Test()
    await test.testing_message()

if __name__ == "__main__":
    asyncio.run(main())