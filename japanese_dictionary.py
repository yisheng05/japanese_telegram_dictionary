"""
Jamdict module for Japanese Dictionary telegram bot

"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
import threading

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
from jamdict import Jamdict
import regex
from sudachipy import tokenizer
from sudachipy import dictionary

# define tokenize mode and tokenizer dictionary
tokenizer_obj = dictionary.Dictionary().create()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hello there, what word may I teach you today?")


def stop(update, context):
    """Send a message when the command /stop is issued."""
    update.message.reply_text("Goodbye and see you again!")


# def help(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')

# Create japDict() - function to lookup in Japanese Dictionary (jmd)
def japDict(update, context):
    jmd = Jamdict()
    ltext = update.message.text
    mode = tokenizer.Tokenizer.SplitMode.C
    for token in tokenizer_obj.tokenize(ltext, mode):
        # if token.dictionary_form() not in ['で', 'に', 'を', 'へ', 'から', 'まで', 'が', 'か', 'の']:
        result = jmd.lookup(token.normalized_form())
        for entry in result.entries[:1]:
            match = regex.search("(?<=\[.*\]).*", str(entry))
            display = match.group()
            update.message.reply_text(display)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1084791658:AAEcB9_2PF0ftRe_n6brOxEogZoxDPt5SzI", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Start the Bot
    dp.add_handler(CommandHandler("start", start))

    # Bot Commands
    # on different japanese inputs, generate lookup output from online dictionary, but wait till start command is given
    dp.add_handler(MessageHandler(Filters.text, japDict))

    # log all errors
    dp.add_error_handler(error)

    # Stop the Bot
    dp.add_handler(CommandHandler("stop", stop))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()
