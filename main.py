import os, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from dotenv import load_dotenv
from database import insert_message
from hashlib import sha256

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

DEJIRBOT_TOKEN = os.getenv('DEJIRBOT_TOKEN')

def start(bot,  update):
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    start_message = f"""سلام {user.first_name} \n
     با این دکمه‌ها می‌تونی کارو شروع کنی:\n
     ثبت پیام تبلیغاتی: /spam
     ثبت پیام غیر تبلیغاتی: /ham

     اگر هم نیاز به کمک یا اطلاعات بیشتر داری: /help
     یا اگر می‌خوای درباره این پروژه بیشتر بدونی: /about
     """
    update.message.reply_text(start_message)

def cancel(bot, update):
    cancel_message = 'فرستادن پیام لغو شد.'
    update.message.reply_text(cancel_message)
    return ConversationHandler.END

# states
msg = range(1)

def spam_callback(bot, update):
    raw_user_id = update.message.from_user.id
    hash_user_id = sha256(str(raw_user_id).encode()).hexdigest()
    
    insert_message(update.message, hash_user_id, "spam")
    spam_submit_message = "با تشکر پیام تبلیغاتی شما ثبت شد"
    update.message.reply_text(spam_submit_message)
    return ConversationHandler.END

def ham_callback(bot, update):
    raw_user_id = update.message.from_user.id
    hash_user_id = sha256(str(raw_user_id).encode()).hexdigest()

    insert_message(update.message, hash_user_id, "ham")
    ham_submit_message = "با تشکر پیام غیرتبلیغاتی شما ثبت شد"
    update.message.reply_text(ham_submit_message)
    return ConversationHandler.END

def help(bot,  update):
    """Send a message when the command /help is issued."""
    help_message = """
    ثبت پیام تبلیغاتی: /spam
    ثبت پیام غیر تبلیغاتی: /ham
    آشنایی با هدف پروژه: /about
    """
    update.message.reply_text(help_message)

def about(bot, update):
    about_message = """
    هدف این ربات چیه؟
    قراره یه مجموعه داده از پیام هایی جمع کنیم که بدون رضایت ما برامون فرستاده می‌شه. مهم‌ترینشون هم اون پیامکهای تبلیغاتی ان که وقت و ناوقت میان و همه مون ازشون دل پری داریم :)
    در نهایت این اطلاعات استفاده می‌شن تا یه نرم افزار پیامک تولید بشه که می‌تونه پیام های تبلیغاتی رو تشخیص بده.
    اگر دوست دارید از این پروژه بیشتر بدونید،
    یا اگر می‌خواید که به ما کمک کنید،
    یا اگر متخصص هوش مصنوعی هستید و می‌خواید به این داده دسترسی داشته باشید،
    برید اینجا:

    https://github.com/payamQorbanpour/dejir
    """
    update.message.reply_text(about_message)

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def get_spam(bot, update):
    get_spam_message = "لطفا پیام تبلیغاتی رو وارد کن."
    update.message.reply_text(get_spam_message)
    return msg

def get_ham(bot, update):
    get_ham_message = "لطفا پیام غیرتبلیغاتی رو وارد کن."
    update.message.reply_text(get_ham_message)
    return msg

def main():
    updater = Updater(DEJIRBOT_TOKEN, use_context=False)

    dp = updater.dispatcher

    spam_handler = ConversationHandler(
        entry_points=[CommandHandler('spam', get_spam), ],
        states={msg: [MessageHandler(Filters.text, spam_callback)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    ham_handler = ConversationHandler(
        entry_points=[CommandHandler('ham', get_ham), ],
        states={msg: [MessageHandler(Filters.text, ham_callback)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(spam_handler)
    dp.add_handler(ham_handler)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("about", about))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
