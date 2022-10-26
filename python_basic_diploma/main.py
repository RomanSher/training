""" Файл для запуска бота. """

import handlers
import literals
from create_bot import bot, logger



if __name__ == '__main__':
    logger.info(literals.BOT_START)
    bot.polling(none_stop=True)
    logger.info(literals.BOT_END)




