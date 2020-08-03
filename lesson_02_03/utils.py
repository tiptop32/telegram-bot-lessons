import shelve
from random import shuffle

from SQLighter import SQLighter
from config import shelve_name, database_name
from telebot import types

def count_rows():
    db = SQLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum

def get_rows_count():
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum

def set_user_game(chat_id, estimated_answer):
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer

def finish_user_game(chat_id):
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]

def get_answer_for_user(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None

def generate_markup(right_answer, wrong_answer):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    all_answers = f'{right_answer},{wrong_answer}'
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)

    shuffle(list_items)

    for item in list_items:
        markup.add(item)
    return markup