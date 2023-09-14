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

def coffee_variable_keyboard():
    print('coffee_variable_keyboard !')




