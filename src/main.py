import logging
import telebot
from res.credentials import BOT_TOKEN
import log_setup

bot = telebot.TeleBot(BOT_TOKEN)

main_logger = log_setup.new_logger('main', logging.DEBUG)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message):
    main_logger.debug(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
