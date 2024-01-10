
import asyncio

from config_reader import config
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.methods.log_out import LogOut
from handlers import bot_messages,handle_film,handle_series,methods
async def main() -> None:


    session = AiohttpSession(
        api=TelegramAPIServer.from_base('http://127.0.0.1:8081')
    )
    print(session.api.base)
    bot = Bot(config.bot_token.get_secret_value(),session=session, parse_mode='HTML')
    dp = Dispatcher(bot=bot,session=session,is_local=True)
    dp.include_routers(
        bot_messages.router,
        handle_film.router,
        handle_series.router,
        methods.router
    )
    print(bot.session.api.base)
    print(bot.session.api.is_local)
    await dp.start_polling(bot,skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
