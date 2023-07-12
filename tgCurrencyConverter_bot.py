import telebot
from telebot import types,util
import re
import requests
import sys

bot = telebot.TeleBot(sys.argv[1])

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_num(str:str):
    return float(re.sub('[^0-9,.]', '', str))

def convert(currencies, from_currency, to_currency, amount): 
    if from_currency != 'USD' : 
        amount = amount / currencies[from_currency] 
    amount = round(amount * currencies[to_currency], 4) 
    return amount

def applyMult(mult:str, n:float) -> float:
    match mult:
        case 'к'        : n *= 1000
        case 'кк'       : n *= 1000000
        case 'ккк'      : n *= 1000000000
        case 'k'        : n *= 1000
        case 'kk'       : n *= 1000000
        case 'kkk'      : n *= 1000000000
        case 'м'        : n *= 1000000
        case 'm'        : n *= 1000000
        case 'тыщ'      : n *= 1000
        case 'тысяч'    : n *= 1000
        case 'косарей'  : n *= 1000
        case 'thousand' : n *= 1000
        case 'тисяча'   : n *= 1000
        case 'млн'      : n *= 1000000
        case 'million'  : n *= 1000000
        case _:
            if mult.startswith('штук'):
                return n * 1000
            if mult.startswith('косар'):
                return n * 1000
            if mult.startswith('тыс'):
                return n * 1000
            if mult.startswith('тыщ'):
                return n * 1000
            if mult.startswith('тис'):
                return n * 1000
            if mult.startswith('tho'):
                return n * 1000
            if mult.startswith('милиа'):
                return n * 1000000000
            if mult.startswith('миллиа'):
                return n * 1000000000
            if mult.startswith('милья'):
                return n * 1000000000
            if mult.startswith('billio'):
               return n * 1000000000
            if mult.startswith('мильё'):
                return n * 1000000
            if mult.startswith('милье'):
                return n * 1000000
            if mult.startswith('мульт'):
                return n * 1000000
            if mult.startswith('милио'):
                return n * 1000000
            if mult.startswith('миллио'):
                return n * 1000000
            if mult.startswith('milli'):
                return n * 1000000
    return n

@bot.message_handler(content_types=["text"])
def handle_text(mes : telebot.types.Message):
    if has_numbers(mes.text):

        main_rule = r"((?:\d*[\.,]\d+|\d+)(\s*))(\s*)([КМГKGM]*|тыс*.+|косар*.+|штук*.+|мульт*.+|thou*.+|мил*.+|(млн)+|mil*.+|bil*.+|\s+)(\s*)*"
        currencies = [
            ['UAH', r"(грив|грн|грi|griv|₴)", '₴'],
            ['EUR', r"(евр|eur|€)"     , '€'],
            ['RUB', r"(руб|rub|₽)"     , '₽'],
            ['USD', r"(дол|dol|\$)"    , '$'],
            ['KZT', r"(тен|teng|₸)"    , '₸'],
            ['CNY', r"(юан|yua|¥)"     , '¥'],
        ]

        s = ''
        for c in currencies:
            res = re.search(main_rule + c[1], mes.text, re.IGNORECASE)
            if res:
                curr = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()['rates']
                n = get_num(res[0])
                mult : str = res[4].lower().strip()
                n = applyMult(mult,n)
                s = f'{n}{c[2]} = '
                for nc in currencies:
                    if c[0] != nc[0]:
                        s += f'{convert(curr,c[0], nc[0], n):,.2f}{nc[2]}  '
                break
        
        if s != '':
            bot.send_message(mes.chat.id, s)
    
bot.infinity_polling(allowed_updates=util.update_types)