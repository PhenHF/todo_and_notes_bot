import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import load_config
from handlers import user_handlers
from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)

async def main():

    logging.basicConfig(
        level = logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    config = load_config()
    bot = Bot(token= config.token, parse_mode='html')
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    #dp.include_router(other_handlers.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__=='__main__':
    asyncio.run(main())