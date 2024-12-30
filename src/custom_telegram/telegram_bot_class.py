from telegram import Bot
import asyncio

class Test:
    def __init__(self) -> None:
        self._telegram_bot = CustomTelegramBot()
        # print(CustomTelegramBot.__api_key)

    async def testing_message(self) -> str:
        print("Sending the request to send a messge \"Testing\"") # Doing Some Synchronous Task

        await self._telegram_bot.send_text("test messaging")

        return "Testing"

class CustomTelegramBot:
    def __init__(
            self,
            api_key: str,
            channel_id: str,
        ) -> None:
        # Get the credential from the json
        # will be considered as private attributes.
        self.__api_key = api_key
        self.__channel_id = channel_id

        # make the bot instance
        self._bot = Bot(self.__api_key)

        return

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

    # await test.testing_message()

if __name__ == "__main__":
    asyncio.run(main())