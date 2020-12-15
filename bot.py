import os, logging
import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PASHIZAK_TOKEN = os.getenv('PASHIZAK_TOKEN')

def db_connection():
    with sqlite3.connect('pashizak.db') as conn:
        return conn

def create_message_table():
    c.execute('''CREATE TABLE message (id int, message text, label text, user_id int, is_approved bool, date text)''')

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

def spam_callback(bot, update):
    insert_spam(update.message)
    update.message.reply_text("با تشکر پیام تبلیغاتی شما ثبت شد")
    return ConversationHandler.END

def nonspam_callback(bot, update):
    insert_nonspam(update.message)
    update.message.reply_text("با تشکر پیام غیرتبلیغاتی شما ثبت شد")
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
    return msg

def insert_spam(msg):  
    c = db_connection() 

    query = f"INSERT INTO message VALUES ('{msg.message_id}','{msg.text}','spam', '1', null, '{msg.date}')"
    c.cursor().execute(query)
    c.commit()
    c.close()

def insert_nonspam(msg):  
    c = db_connection() 

    query = f"INSERT INTO message VALUES ('{msg.message_id}','{msg.text}','nonspam', '1', null, '{msg.date}')"
    c.cursor().execute(query)
    c.commit()
    c.close()

def main():
    updater = Updater(PASHIZAK_TOKEN, use_context=False)

    dp = updater.dispatcher

    spam_handler = ConversationHandler(
        entry_points=[CommandHandler('spam', get_spam), ],
        states={msg: [MessageHandler(Filters.text, spam_callback)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    nonspam_handler = ConversationHandler(
        entry_points=[CommandHandler('nonspam', get_nonspam), ],
        states={msg: [MessageHandler(Filters.text, nonspam_callback)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(spam_handler)
    dp.add_handler(nonspam_handler)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("nonspam", get_nonspam))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
