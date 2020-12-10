#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

conn = sqlite3.connect('pashizak.db')


c = conn.cursor()
# c.execute('''CREATE TABLE message
#              (id int, message text, label text, user_id int, is_approved bool, date text)''')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(bot,  update):
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    hello_message = f"سلام {user.first_name} \n برای ثبت پیام تبلیغاتی دکمه /spam و برای ثبت پیام غیرتبلیغاتی دکمه /nonspam رو بزن"
    update.message.reply_text(hello_message)


def cancel(bot, update):
    update.message.reply_text('فرستادن پیام لغو شد.')
    return ConversationHandler.END


# states
msg = range(1)

def callback(bot, update):
    update.message.reply_text("با تشکر")
    return ConversationHandler.END

def help(bot,  update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')  

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def get_spam(bot, update):
    update.message.reply_text("لطفا پیام تبلیغاتی رو وارد کن.")
    return msg

def get_nonspam(bot, update):
    update.message.reply_text("لطفا پیام غیرتبلیغاتی رو وارد کن.")

# def insert_message():
#     msg = update.message
    
#     # Insert a row of data
#     query = f"INSERT INTO message VALUES ('{msg.id}','{msg.text}','spam', '1', null, '{msg.date}')"
#     c.execute(query)

#     # Save (commit) the changes
#     conn.commit()

#     # We can also close the connection if we are done with it.
#     # Just be sure any changes have been committed or they will be lost.
#     conn.close()

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=False)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('spam', get_spam), ],
        states={msg: [MessageHandler(Filters.text, callback)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("nonspam", get_nonspam))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
