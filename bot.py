import logging
from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram.utils.helpers import escape_markdown
from reciever import return_summary

# Read token
f = open("token", "r")
TOKEN = f.readline()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi, I'm Summer!")


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Type:\n\n/summarize anything you wish\n\nto get started.")


def summarize(update, context):
    """Summarize the user's query."""
    summary = return_summary(update.message.text[10:])
    update.message.reply_text(summary)


def inlinequery(update, context):
    query = update.inline_query.query
    print(query)
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="summarize: " + query,
            input_message_content=InputTextMessageContent(
                query + "\n" + return_summary(query)[:1024 - len(query) - 2]))
        ]
    update.inline_query.answer(results)


def error_callback(update, context):
    update.message.reply_text("error")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("summarize", summarize))

    # on noncommand i.e message - summarize the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, summarize))
    dp.add_handler(InlineQueryHandler(inlinequery))

    # on error - print error
    # dp.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
