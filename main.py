import asyncio
from aiogram import Dispatcher
from config import bot, storage
from handlers import start, sms, call

async def main():
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        start.router,
        sms.router,
        call.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("aiogram").setLevel(logging.INFO)
    print("Bot is starting...")
    asyncio.run(main())

