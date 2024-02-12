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
from TelegramKeyboard import (
    cafe_choice_keyboard,
    main_keyboard,
    coffee_variable_keyboard,
    coffee_choice_keyboard,
    show_basket_keyboard,
    start_keyboard
                              )

from BotMessage import (
    err_call_ship_msg,
    err_send_ship_msg,
    successful_pay_msg
)

import threading
import datetime
import time
from config import bot_key, provider_key
from CreateClientCard import Client
from GetPosterData import Product
from CreateTranscription import Transcription
import logging


logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
sessions = dict()
start_time = datetime.time(8, 0)
end_time = datetime.time(21, 0)


def start_message(update: Update, context: CallbackContext):
    user = Client()
    transcription_id = 0
    cafe_id = 0
    username = update.message.from_user.username
    client_id = user.create_client(username)
    sessions[update.message.chat_id] = (client_id, transcription_id, cafe_id)
    print(sessions)
    update.message.reply_text("Привіт!", reply_markup=start_keyboard())


def hello(update: Update, context: CallbackContext):
    print('hello RUN')
    current_time = datetime.datetime.now().time()
    d = dispatcher
    spots = Product()
    data = spots.get_spots()
    if start_time <= current_time <= end_time:
        update.callback_query.message.edit_text("Оберіть заклад для замовлення:",
                                                reply_markup=cafe_choice_keyboard(data, d, create_transcription))

    else:
        update.callback_query.message.reply_text("Привіт ! Зараз не робочий час, бот працює з 8-20:00,"
                                                 " чекаємо на вас пізніше 🤍")


def create_transcription(update: Update, context: CallbackContext):
    global sessions
    print("create_transcription ------> run !")
    cafe_id = update['callback_query']['data']
    client_id = sessions[update.callback_query.from_user.id][0]
    trans = Transcription()
    trans_id = trans.create_t(cafe_id)
    trans.add_client(cafe_id, trans_id, client_id)

    existing_tuple = sessions[update.callback_query.from_user.id]
    new_tuple = (existing_tuple[0], existing_tuple[1], cafe_id, trans_id)
    sessions[update.callback_query.from_user.id] = new_tuple
    print(sessions)
    update.callback_query.message.edit_text('MENU', reply_markup=main_keyboard())

    def del_t_timer():
        global sessions
        t_status = trans.get_t_status(trans_id)
        if t_status == '1':
            trans.remove_t(trans_id)
            print("The check was automatically deleted, id: ", trans_id)
            update.callback_query.message.reply_text("Час очікування вийшов. Ваш чек видалено !")
            sessions = dict()
        else:
            pass

    threading.Timer(1800, del_t_timer).start()
    return sessions


def back_to_main_menu(update: Update, context: CallbackContext):
    global sessions
    trans_id = sessions[update.callback_query.from_user.id][3]
    del_tr = Transcription()
    del_tr.remove_t(trans_id)
    hello(update, context)

    return sessions


def coffee_menu_choice(update: Update, context: CallbackContext):
    print('coffee_menu_choice is running !')
    coffee_category = Product()
    data = coffee_category.get_drink_category()
    print(data)
    d = dispatcher

    update.callback_query.message.edit_text('Кава та напої:',
                                            reply_markup=coffee_variable_keyboard(data, d, coffee_choice))


def breakfast_menu_choice(update: Update, context: CallbackContext):
    print('breakfast_menu_choice is running !')


def coffee_choice(update: Update, context: CallbackContext):
    choice = update['callback_query']['data']
    print('coffee_choice is running, data:', choice)
    d = dispatcher
    drink = Product()
    data = drink.get_drink_data(choice)
    update.callback_query.message.edit_text(str(choice) + ':',
                                            reply_markup=coffee_choice_keyboard(data, d, add_drink_in_trans))


def add_drink_in_trans(update: Update, context: CallbackContext):
    choice = update['callback_query']['data']
    print('add_drink_in_trans is running ! data:', choice)
    cafe_id = sessions[update.callback_query.from_user.id][2]
    transcription_id = sessions[update.callback_query.from_user.id][3]
    user = Transcription()
    user.add_drink(cafe_id, transcription_id, choice)
    message = update.callback_query.message.reply_text("Товар додано 👌")

    def delete_message():
        message.delete()
    threading.Timer(3, delete_message).start()


def show_basket(update: Update, context: CallbackContext):
    print('show_basket is running!')
    transaction_id = sessions[update.callback_query.from_user.id][3]
    d = dispatcher
    user = Transcription()
    data = user.get_t(transaction_id)
    print(data)
    message = 'Ваш кошик : \n\n'

    for product, (price, num) in data.items():
        message += f"{product}\t{price}грн x {num}шт\n"
    update.callback_query.message.edit_text(message,
                                            reply_markup=show_basket_keyboard(data, d))


def start_shipping_callback(update: Update, context: CallbackContext) -> None:

    if update.callback_query.from_user.id not in sessions:
        print('error: msg from unknown user!')
        return
    (_, _, suma) = sessions[update.callback_query.from_user.id]
    if suma:
        chat_id = update.callback_query.from_user.id
        title = 'Оплата Замовлення "Заберу сам"'
        description = final_check
        payload = 'Custom-Payload'
        provider_token = provider_key
        currency = 'UAH'
        price = suma
        prices = [LabeledPrice('Test', price * 100)]
        context.bot.send_invoice(
            chat_id, title, description, payload, provider_token, currency, prices
            )
    else:
        update.callback_query.message.reply_text(err_send_ship_msg())


def shipping_callback(update: Update, context: CallbackContext):
    query = update.shipping_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message=err_call_ship_msg())
        return


def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message=err_call_ship_msg())
    else:
        query.answer(ok=True)


def successful_payment_callback(update: Update, context: CallbackContext):
    update.message.reply_text(successful_pay_msg())







############################### Handlers #############################################

updater = Updater(bot_key, use_context=True)
dispatcher = updater.dispatcher

# Start the Bot
updater.start_polling()

dispatcher.add_handler(CommandHandler("start", start_message))
dispatcher.add_handler(CallbackQueryHandler(hello, pattern='hello'))
dispatcher.add_handler(CallbackQueryHandler(coffee_menu_choice, pattern='COFFEE'))
#dispatcher.add_handler(CallbackQueryHandler(breakfast_menu_choice, pattern='BREAKFAST'))
dispatcher.add_handler(CallbackQueryHandler(back_to_main_menu, pattern='back_to_main'))
dispatcher.add_handler(CallbackQueryHandler(back_to_main_menu, pattern='clear_basket'))
dispatcher.add_handler(CallbackQueryHandler(coffee_menu_choice, pattern='back_to_coffe_variable'))
dispatcher.add_handler(CallbackQueryHandler(show_basket, pattern='basket'))
dispatcher.add_handler(CallbackQueryHandler(start_shipping_callback, pattern='pay'))
# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.


if __name__ == '__main__':
    updater.start_polling()
