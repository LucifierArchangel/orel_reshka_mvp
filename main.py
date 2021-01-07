import json
import time
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from random import randint

from users_controller import UsersController

users_controller = UsersController('db/users.json')

config = json.loads(open('config.json', 'r').read())

token = config['token']

bot = TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    text = message.text.split(' ')

    ref = 0
    if len(text) == 2:
        try:
            ref = int(text[1])
        except:
            pass

    username = message.from_user.username
    user_id = message.from_user.id

    users_controller.add_user(username, user_id, ref)

    msg = """*Добро пожаловать в игру Орели и Решка*
    У вас есть демо-баланс на 100 едениц, используйте с умом
    """

    keyboard = InlineKeyboardMarkup()

    buttons = [
        [
            {'text': 'Инфо', 'callback_data': 'gminfo'},
            {'text': 'Информация о профиле', 'callback_data': 'profile_info'}
        ],
        [
            {'text': 'Играть', 'callback_data': 'play'},
            {'text': 'Пополнить баланс', 'callback_data': 'payment'}
        ]
    ]

    for row in buttons:
        btns = [
            InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']) for btn in row
        ]

        keyboard.add(*btns)

    bot.send_message(message.chat.id, msg, reply_markup=keyboard, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        data = call.data
        args = data.split('/')

        if args[0] == 'gminfo':
            msg = """*Орел и Решка*
                MVP проекта для Лиса
                """

            keyboard = InlineKeyboardMarkup()

            buttons = [
                [
                    {'text': 'Назад', 'callback_data': 'main_menu'},
                ]
            ]

            for row in buttons:
                btns = [
                    InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']) for btn in row
                ]

                keyboard.add(*btns)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='Markdown', reply_markup=keyboard)
        elif args[0] == 'main_menu':
            msg = """*Добро пожаловать в игру Орели и Решка*
            У вас есть демо-баланс на 100 едениц, используйте с умом
            """

            keyboard = InlineKeyboardMarkup()

            buttons = [
                [
                    {'text': 'Инфо', 'callback_data': 'gminfo'},
                    {'text': 'Информация о профиле', 'callback_data': 'profile_info'}
                ],
                [
                    {'text': 'Играть', 'callback_data': 'play'},
                    {'text': 'Пополнить баланс', 'callback_data': 'payment'}
                ]
            ]

            for row in buttons:
                btns = [
                    InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']) for btn in row
                ]

                keyboard.add(*btns)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='Markdown', reply_markup=keyboard)

        elif args[0] == 'profile_info':
            user = users_controller.find_user_by_user_id(call.from_user.id)
            
            msg = "*Username*: %s\n" % (user['username']) 
            msg += "*User ID*: %i\n" % (user['user_id'])
            msg += "*Balance*: %f\n" % (user['balance'])
            msg += "*Ref ID*: %i\n" % (user['ref'])

            keyboard = InlineKeyboardMarkup()

            buttons = [
                [
                    {'text': 'Назад', 'callback_data': 'main_menu'},
                ],
                [
                    {'text': 'Пополнить баланс', 'callback_data': 'payment'}
                ]
            ]

            for row in buttons:
                btns = [
                    InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']) for btn in row
                ]

                keyboard.add(*btns)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='Markdown', reply_markup=keyboard)
        elif args[0] == 'payment':
            msg = 'Попление баланса в разработке'

            keyboard = InlineKeyboardMarkup()

            buttons = [
                [
                    {'text': 'Назад', 'callback_data': 'main_menu'},
                ]
            ]

            for row in buttons:
                btns = [
                    InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']) for btn in row
                ]

                keyboard.add(*btns)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='Markdown', reply_markup=keyboard)

        elif args[0] == 'play':
            msg = 'Сделайте ставку:'

            keyboard = InlineKeyboardMarkup()

            buttons = [
                [
                    {'text': '100', 'callback_data': 'st/100'},
                    {'text': '200', 'callback_data': 'st/200'},
                ],
                [
                    {'text': '300', 'callback_data': 'st/300'},
                    {'text': '400', 'callback_data': 'st/400'},
                ],
                [
                    {'text': 'Назад', 'callback_data': 'main_menu'},
                ]
            ]

            for row in buttons:
                btns = [
                    InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']) for btn in row
                ]

                keyboard.add(*btns)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='Markdown', reply_markup=keyboard)
        elif args[0] == 'st':
            msg = ''
            buttons = []
            user = users_controller.find_user_by_user_id(call.from_user.id)
            st = int(args[1])
            if st > user['balance']:
                msg = 'Недостаточно средтсв'
                buttons = [
                [
                    {'text': 'Назад', 'callback_data': 'play'},
                ]
            ]
            else:
                msg = 'Ваша ставка: ' + args[1]
                msg += 'Выберите исход:'
                buttons = [
                [
                    {'text': 'Орел', 'callback_data': 'select/' + args[1] + '/0'},
                    {'text': 'Решка', 'callback_data': 'select/' + args[1] + '/1'},
                ],
                [
                    {'text': 'Назад', 'callback_data': 'play'},
                ]
            ]

            keyboard = InlineKeyboardMarkup()


            for row in buttons:
                btns = [
                    InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']) for btn in row
                ]

                keyboard.add(*btns)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='Markdown', reply_markup=keyboard)
        elif args[0] == 'select':
            user = users_controller.find_user_by_user_id(call.from_user.id)
            print(user)
            exodus = randint(0, 100)

            msg = ''

            st = int(args[1])
            select = int(args[2])

            print(user['username'], st, select, exodus)

            if exodus > 50:
                print('q')
                if select == 1:
                    msg += 'Вы выиграли'
                    balance = user['balance'] + st
                    users_controller.change_balance(call.from_user.id, balance)
                else:
                    msg += 'Вы проиграли'
                    balance = user['balance'] - st
                    users_controller.change_balance(call.from_user.id, balance)

            else:
                print('qq')
                if select == 0:
                    msg += 'Вы выиграли'
                    balance = user['balance'] + st
                    users_controller.change_balance(call.from_user.id, balance)
                else:
                    msg += 'Вы проиграли'
                    balance = user['balance'] - st
                    users_controller.change_balance(call.from_user.id, balance)

            print('pre keyboard')

            keyboard = InlineKeyboardMarkup()

            print('pre buttons')

            buttons = [
                [
                    {'text': 'Назад', 'callback_data': 'main_menu'},
                ]
            ]

            print('pre adding buttons')

            for row in buttons:
                btns = [
                    InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']) for btn in row
                ]

                keyboard.add(*btns)

            print('pre edit')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='Markdown', reply_markup=keyboard)

bot.infinity_polling()