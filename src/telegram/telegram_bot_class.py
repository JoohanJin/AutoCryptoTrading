from telegram import Bot
import json
import asyncio


class Test:
    def __init__(self) -> None:
        self._telegram_bot = TelegramBot()

    async def print_hello_world(self) -> str:
        print("Hello World") # Doing Some Synchronous Task

        await self._telegram_bot.send_text("Hello World")

        return "Hello World"

class TelegramBot:
    def __init__(self) -> None:
        # Get the credential from the json
        # will be considered as private attributes.
        self.__api_key, self.__channel_id = self.get_credential()
        
        # make the bot instance
        self._bot = Bot(self.__api_key)
        return

    def get_credential(self) -> str:
        # funcion called when TelegramBot is initialized.
        f = open('key.json')
        data = json.load(f)
        return data['api_key'], data['channel_id']

    async def send_text(self, message: str) -> None:
        await self._bot.send_message(
            chat_id = self.__channel_id,
            text = message,
        )
        return


############################################################################################
#                                     Running Code Zone                                    #
############################################################################################

async def main():
    test = Test()
    await test.print_hello_world()


if (__name__ == "__main__"):
    asyncio.run(main())