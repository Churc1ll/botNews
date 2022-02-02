from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

TOKEN = os.environ["TOKEN"]

chatId = -1001546899691
# chatId = -755407856

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    botMessage()


def echo(update, context):
    botMessage()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    # updater = Updater(TOKEN, use_context=True)

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

    # botMessage()
    updater.idle()


updater = Updater(TOKEN, use_context=True)


def botMessage():
    from parse import message
    ret_msg = updater.bot.sendMessage(
        chat_id=chatId, text=message, parse_mode="Markdown")
    assert ret_msg.message_id

 
if __name__ == '__main__':
    main()


# while True:
#     time.sleep( 86400 )
    # sleep to avoid running the function again in the next loop


# schedule.every(1).day.do(botMessage)
# or
# schedule.every().day.at("13:25").do(botMessage)

# schedule version

# while True:
#     schedule.run_pending()
#     time.sleep(1)
