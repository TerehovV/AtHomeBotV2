from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from GetPosterData import Product


def start_keyboard():
    print('start_keyboard is running !')
    keyboard = [[InlineKeyboardButton(text='Розпочати роботу', callback_data='hello')],
                [InlineKeyboardButton(text='Y', callback_data='hello')]]

    return InlineKeyboardMarkup(keyboard)


def cafe_choice_keyboard(data, d, create_transcription):
    print('cafe_choice_keyboard is running !')
    inl = InlineKeyboardButton
    keyboard = []
    for i in data:
        print(i)
        print(data[i])
        x = [inl(text=str(data[i]), callback_data=str(i))]
        keyboard.append(x)
        d.add_handler(CallbackQueryHandler(create_transcription, pattern=str(i)))

    return InlineKeyboardMarkup(keyboard)


def main_keyboard():
    print('main_keyboard is running !')

    keyboard = [[InlineKeyboardButton(text='Кава та напої', callback_data='COFFEE')],
                [InlineKeyboardButton(text='Кухня (Сніданки) BETA !!!', callback_data='BREAKFAST')],
                [InlineKeyboardButton(text='Назад ↩', callback_data='back_to_main')]]

    return InlineKeyboardMarkup(keyboard)


def coffee_variable_keyboard(data, d, coffee_choice):
    print('coffee_variable_keyboard is running!')
    inl = InlineKeyboardButton
    keyboard = []
    for i in data:
        x = [inl(text=str(data[i]), callback_data=data[i])]
        keyboard.append(x)
        d.add_handler(CallbackQueryHandler(coffee_choice, pattern=data[i]))

    y = [inl(text='Кошик 🛒', callback_data='basket'),
         inl(text='Назад ↩', callback_data='back_to_main')]
    keyboard.append(y)

    return InlineKeyboardMarkup(keyboard)


def coffee_choice_keyboard(data, d, add_drink_in_trans):
    print('coffee_choice_keyboard is running!')
    inl = InlineKeyboardButton
    keyboard = []
    print(data)
    for i in data:
        x = [inl(text=str(i), callback_data=data[i])]
        keyboard.append(x)
        d.add_handler(CallbackQueryHandler(add_drink_in_trans, pattern=data[i]))

    y = [inl(text='Кошик 🛒', callback_data='basket'),
         inl(text='Назад ↩', callback_data='back_to_coffe_variable')]
    keyboard.append(y)

    return InlineKeyboardMarkup(keyboard)


def show_basket_keyboard(data, d):
    print('show_basket_keyboard is running!')
    print(data)
    keyboard = [[InlineKeyboardButton(text='Сплатити', callback_data='pay')],
                [InlineKeyboardButton(text='Очистити кошик', callback_data='clear_basket')]]

    return InlineKeyboardMarkup(keyboard)



