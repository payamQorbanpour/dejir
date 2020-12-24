import os
import unittest
from main import get_spam, spam_callback, cancel
from dotenv import load_dotenv
from telegram import (
    Chat,
    User,
    Message,
    MessageEntity,
    Update
)
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
    CommandHandler,
    Updater
)

load_dotenv()
DEJIRBOT_TOKEN = os.getenv('DEJIRBOT_TOKEN')

msg = range(1)

def user1():
    return User(first_name='Mester Tester', id=1212, is_bot=False)

class TestSpam(unittest.TestCase):
    group = Chat(0, Chat.GROUP)

    def test_get_spam(self):
        updater = Updater(DEJIRBOT_TOKEN, use_context=False)

        dp = updater.dispatcher
        
        spam_handler = ConversationHandler(
            entry_points=[CommandHandler('spam', get_spam), ],
            states={msg: [MessageHandler(Filters.text, spam_callback)]},
            fallbacks=[CommandHandler('cancel', cancel)]
        )
        
        dp.add_handler(spam_handler)

        message = Message(
            0,
            None,
            self.group,
            from_user=user1,
            text='/start',
            entities=[
                MessageEntity(type=MessageEntity.BOT_COMMAND, offset=0, length=len('/start'))
            ],
            # bot=bot,
        )
        dp.process_update(Update(update_id=0, message=message))
        assert len(spam_handler.conversations) == 0


if __name__ == "__main__":
    unittest.main()

