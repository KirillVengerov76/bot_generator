import telebot
from telebot import types
from json import load, dumps
from TelegramBotData import *

bot = telebot.TeleBot(config.BotKey)

inventory.Inventory.node = config.node
inventory.Inventory.size = config.inventory_size
inventory.Inventory.visit_req = [[] for _ in range(inventory.Inventory.node)]
inventory.Inventory.inventory_req = [[] for _ in range(inventory.Inventory.node)]

reverse_button = {}

with open('TelegramBotData/text.json') as fp:
    text = load(fp)
with open('TelegramBotData/adjacency_list.json') as fp:
    inventory.adjacency_list = load(fp)
with open('TelegramBotData/button.json') as fp:
    button = load(fp)
with open('TelegramBotData/save.json') as fp:
    save = load(fp)
with open('TelegramBotData/inventory_list.json', 'r') as fp:
    inventory_list = load(fp)
with open('TelegramBotData/visited_req_list.json', 'r') as fp:
    for v, u in load(fp):
        inventory.Inventory.set_visit_req(v, u)
with open('TelegramBotData/inventory_req_list.json', 'r') as fp:
    for v, j in load(fp):
        inventory.Inventory.set_inventory_req(v, j)

for i in button:
    for v, k in enumerate(i):
        reverse_button[k] = v


def save_wrapper(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        open('TelegramBotData/save.json', 'w').write(dumps(save, indent=4, ensure_ascii=False))

    return wrapper


@bot.message_handler(commands=['start'])
@save_wrapper
def any_msg(message):
    client_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    vertex = 0
    inv = inventory.Inventory()
    inv.visit_add(vertex)
    save[client_id] = [vertex, inv.__dict__]
    bot.send_message(message.chat.id, "Нажми на команду /restart", reply_markup=keyboard)


@bot.message_handler(commands=['restart'])  # Начать заново
@save_wrapper
def any_msg(message):
    client_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_remove = telebot.types.ReplyKeyboardRemove()
    vertex = 0
    inv = inventory.Inventory()
    inv.visit_add(vertex)
    bot.send_message(message.chat.id, text[0], reply_markup=keyboard_remove)
    for possible_vertex in inventory.adjacency_list[vertex]:  # Добавление всех кнопок
        if inv.check(vertex, possible_vertex):
            keyboard.add(types.KeyboardButton(text=button[vertex][possible_vertex]))
    bot.send_message(message.chat.id, 'Что будете делать;)?', reply_markup=keyboard)
    save[client_id] = [vertex, inv.__dict__]


@bot.message_handler(content_types=["text"])
@save_wrapper
def any_msg(message):
    client_id = message.chat.id
    keyboard_remove = telebot.types.ReplyKeyboardRemove()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text not in reverse_button.keys():
        bot.send_message(message.chat.id, "Жмякай кнопки падла!", reply_markup=keyboard)
        return
    new_vertex = reverse_button[message.text]
    current_vertex = save[client_id][0]
    inv = inventory.Inventory()
    print(current_vertex, new_vertex)
    inv.__dict__ = save[client_id][1]
    inv.visit_add(new_vertex)
    for item in inventory_list[new_vertex]:
        inv.inventory_add(item)
    if new_vertex not in inventory.adjacency_list[current_vertex]:
        bot.send_message(message.chat.id, f"Жмякай кнопки падла!", reply_markup=keyboard)
        return
    if not inv.check(current_vertex, new_vertex):
        bot.send_message(message.chat.id, "Ты не можешь это сделать!", reply_markup=keyboard)
        return
    bot.send_message(message.chat.id, text[new_vertex], reply_markup=keyboard_remove)

    for possible_vertex in inventory.adjacency_list[new_vertex]:
        if inv.check(new_vertex, possible_vertex):
            keyboard.add(types.KeyboardButton(text=button[new_vertex][possible_vertex]))

    inv.visit_add(new_vertex)
    bot.send_message(message.chat.id, 'Что будете делать;)?', reply_markup=keyboard)
    save[client_id] = [new_vertex, inv.__dict__]


print(f'{text=}')
print(f'{inventory.adjacency_list=}')
print(f'{save=}')
print(f'{button=}')
print(f'{reverse_button=}')
print(f'{config.BotKey=}')
print(f'{inventory_list=}')
print(f'{inventory.Inventory.visit_req=}')
print(f'{inventory.Inventory.inventory_req=}')
input()
