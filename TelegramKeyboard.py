from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from GetPosterData import Product


def cafe_choice_keyboard():
    print('cafe_choice_keyboard is running !')
    keyboard = [[InlineKeyboardButton(text='Вишгородська 45 (Над Варусом)', callback_data='VISH')],
                [InlineKeyboardButton(text='Червонопільска 2Г ("Паркова Вежа") ', callback_data='KRAS')]]
    return InlineKeyboardMarkup(keyboard)


def main_keyboard():
    print('main_keyboard is running !')
    keyboard = [[InlineKeyboardButton(text='Кава та напої', callback_data='COFFEE')],
                [InlineKeyboardButton(text='Кухня (Сніданки)', callback_data='BREAKFAST')]]
    return InlineKeyboardMarkup(keyboard)


def coffee_variable_keyboard(data, d, coffee_choice):
    print('coffee_variable_keyboard is running!')
    inl = InlineKeyboardButton
    keyboard = []
    for i in data:
        x = [inl(text=str(data[i]), callback_data=data[i])]
        keyboard.append(x)
        d.add_handler(CallbackQueryHandler(coffee_choice, pattern=data[i]))

    y = [inl(text='Назад ↩', callback_data='back_to_main')]
    keyboard.append(y)

    return InlineKeyboardMarkup(keyboard)


def coffee_choice_keyboard(data, d, create_transcription):
    print('coffee_choice_keyboard is running!')
    inl = InlineKeyboardButton
    keyboard = []
    print(data)
    for i in data:
        x = [inl(text=str(i), callback_data=data[i])]
        keyboard.append(x)
        d.add_handler(CallbackQueryHandler(create_transcription, pattern=data[i]))

    y = [inl(text='Назад ↩', callback_data='back_to_coffe_variable')]
    keyboard.append(y)

    return InlineKeyboardMarkup(keyboard)


