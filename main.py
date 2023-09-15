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
from TelegramKeyboard import cafe_choice_keyboard, main_keyboard, coffee_variable_keyboard
from config import bot_key, provider_key
from CreateClientCard import Client
from GetPosterData import Product
import logging


logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
sessions = dict()


def hello(update: Update, context: CallbackContext):
    user = Client()
    transcription_id = 0
    cafe_id = 0
    update.message.reply_text("Привіт!")
    update.message.reply_text("Оберіть заклад для замовлення:",
                              reply_markup=cafe_choice_keyboard())
    global sessions
    username = update.message.from_user.username
    client_id = user.create_client(username)
    sessions[update.message.chat_id] = (client_id, transcription_id, cafe_id)
    print(sessions)


def change_cafe_to_vish(update: Update, context: CallbackContext):
    global sessions
    existing_tuple = sessions[update.callback_query.from_user.id]
    new_tuple = (existing_tuple[0], existing_tuple[1], 2)
    sessions[update.callback_query.from_user.id] = new_tuple
    print(sessions)
    update.callback_query.message.edit_text('Меню Вишгородьска 45', reply_markup=main_keyboard())
    return sessions


def change_cafe_to_kras(update: Update, context: CallbackContext):
    global sessions
    existing_tuple = sessions[update.callback_query.from_user.id]
    new_tuple = (existing_tuple[0], existing_tuple[1], 1)
    sessions[update.callback_query.from_user.id] = new_tuple
    print(sessions)
    update.callback_query.message.edit_text('Меню Червонопільска 2Г', reply_markup=main_keyboard())
    return sessions


def back_to_main_menu(update: Update, context: CallbackContext):
    if sessions[update.callback_query.from_user.id][2] == 1:
        change_cafe_to_kras(update, context)
    elif sessions[update.callback_query.from_user.id][2] == 2:
        change_cafe_to_vish(update, context)
    else:
        pass


def coffee_menu_choice(update: Update, context: CallbackContext):
    print('coffee_menu_choice is running !')
    coffee_category = Product()
    data = coffee_category.get_drink_category()
    print(data)
    d = dispatcher

    update.callback_query.message.edit_text('Кава та напої:', reply_markup=coffee_variable_keyboard(data, d, coffee_choice))


def breakfast_menu_choice(update: Update, context: CallbackContext):
    print('breakfast_menu_choice is running !')


def coffee_choice(update: Update, context: CallbackContext):
    print('coffee_choice is running !')

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
dispatcher.add_handler(CallbackQueryHandler(back_to_main_menu, pattern='back_to_main'))
# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.


if __name__ == '__main__':
    updater.start_polling()
