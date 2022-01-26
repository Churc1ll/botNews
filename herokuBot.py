
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os


import telebot

import requests
from bs4 import BeautifulSoup

import re

import schedule
import datetime
import time

chatId = -1001546899691


PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5010883386:AAGjmE4-q6WDcinGkFGjVfSU4kpna8Q7eEc'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# my


def date():
    now = datetime.datetime.now()
    return '0' + str(now.day) if len(str(now.day)) < 2 else str(now.day) + '. ' + '0' + str(now.month) if len(str(now.month)) < 2 else str(now.month) + ' ' + now.hour


def parse(url, tag, details):
    response = requests.get(url)
    answer = BeautifulSoup(response.text, 'lxml')
    return answer.find_all(tag, details)


def corona():
    quote = parse(
        'https://coronavirus-monitorus.ru/moskva/',
        'sup',
        ''
    )[0]
    answ = re.findall(r'\d+', str(quote))

    return ' '.join(answ)


def bitcoin():
    quote = parse(
        'https://www.rbc.ru/crypto/currency/btcusd',
        'span',
        'currencies__td__inner'
    )[1]
    sum = ''.join(re.findall(r'\d+', str(quote)))

    return sum[0:2] + ' ' + sum[2:5] + ',' + (sum[5:] if len(sum) > 6 else '00')


def dollar():
    quote = parse(
        'https://quote.rbc.ru/ticker/72413',
        'span',
        'chart__info__sum'
    )
    sum = ''.join(re.findall(r'\d+', str(quote)))

    return sum[0:2] + ',' + sum[2:]


def message():
    return 'На *' + date() + '* количество зараженных по Москве:  *' + corona() + '*' + ' человек\n\nКурс доллара: ' + '*' + dollar() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'


mess = message()


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(
        'https://fathomless-brushlands-82588.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.

    # updater.idle()

    # updater.bot.sendMessage(
    #     chat_id=chatId, text=mess)

    def botMessage():
        updater.bot.sendMessage(
            chat_id=chatId, text=mess)
    # botMessage()
    schedule.every(1).minutes.day.do(botMessage)

    # schedule.every().day.at("13:25").do(botMessage)

    while True:
        schedule.run_pending()
        time.sleep(1)


updater = Updater(TOKEN, use_context=True)


def botMessage():
    updater.bot.sendMessage(
        chat_id=chatId, text=mess)


start_time = datetime.datetime.now()
interval = start_time + datetime.timedelta(minutes=1)

# dynamically create the interval times
tweet_times = [start_time.minute, interval.minute]
# botMessage()

if __name__ == '__main__':
    main()


while True:
    current_time = datetime.datetime.now()
    if current_time.minute in tweet_times:
        # your function that tweets
        botMessage()
        # sleep to avoid running the function again in the next loop
        time.sleep(50)


# botMessage()
# schedule.every(1).minutes.day.do(botMessage)


# while True:
#     schedule.run_pending()
#     time.sleep(1)
