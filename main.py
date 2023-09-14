
from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    CallbackContext,
    CallbackQueryHandler
)
from TelegramKeyboard import cafe_choice_keyboard, main_keyboard
from config import bot_key, provider_key
from CreateClientCard import Client
import logging


logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
sessions = dict()


def hello(update: Update, context: CallbackContext):
    user = Client()
    cafe_id = 0
    update.message.reply_text("Привіт!")
    update.message.reply_text("Оберіть заклад для замовлення:",
                              reply_markup=cafe_choice_keyboard())

    global sessions
    username = update.message.from_user.username
    client_id = user.create_client(username)
    sessions[update.message.chat_id] = (username, client_id, cafe_id)
    print(sessions)


def change_cafe_to_vish(update: Update, context: CallbackContext):
    global sessions
    existing_tuple = sessions[update.callback_query.from_user.id]
    new_tuple = (existing_tuple[0], existing_tuple[1], 2)
    sessions[update.callback_query.from_user.id] = new_tuple
    print(sessions)
    update.callback_query.message.edit_text('Молодець', reply_markup=main_keyboard())
    return sessions


def change_cafe_to_kras(update: Update, context: CallbackContext):
    global sessions
    existing_tuple = sessions[update.callback_query.from_user.id]
    new_tuple = (existing_tuple[0], existing_tuple[1], 1)
    sessions[update.callback_query.from_user.id] = new_tuple
    print(sessions)
    update.callback_query.message.edit_text('Молодець', reply_markup=main_keyboard())
    return sessions


def coffee_menu_choice(update: Update, context: CallbackContext):
    print('coffee_menu_choice is running !')


def breakfast_menu_choice(update: Update, context: CallbackContext):
    print('breakfast_menu_choice is running !')


############################### Handlers #############################################

updater = Updater(bot_key)
dispatcher = updater.dispatcher

# Start the Bot
updater.start_polling()

dispatcher.add_handler(CommandHandler("start", hello))
dispatcher.add_handler(CallbackQueryHandler(change_cafe_to_vish, pattern='VISH'))
dispatcher.add_handler(CallbackQueryHandler(change_cafe_to_kras, pattern='KRAS'))
dispatcher.add_handler(CallbackQueryHandler(coffee_menu_choice, pattern='COFFEE'))
dispatcher.add_handler(CallbackQueryHandler(breakfast_menu_choice, pattern='BREAKFAST'))

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()


if __name__ == '__main__':
    updater.polling()