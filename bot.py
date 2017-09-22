import logging
import telegram
from telegram.error import NetworkError, Unauthorized
import telebot
from time import sleep
import os
import dataset as ds
import requests
import json
import pandas as pd
import datetime
import time

from telebot import types
import app.DB_func as db
from app.cnf import db_url, qiwi_token, bot_token, qw_login
import app.vk_api_operations as vk
import app.telegram_func as tl
import app.qw_api_operations as qw

# INIT
token = bot_token
bot = telebot.TeleBot(token)
user_dict = {}
user_step = {}
user_init = {}
exist_user_dict = {}
user_step["test"] = None

hello_msg = """Добро пожаловать в Pennyjob! Нажмите /help для справки. \nЧтобы получить задание, нажмите /job"""

### Begin

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    try:
        bot.send_message(chat_id, text=hello_msg, reply_markup=types.ReplyKeyboardRemove())
    except:
        bot.send_message(chat_id, text=hello_msg)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    chat_id = message.chat.id
    #itembtn1 = types.KeyboardButton('ОК')
    help_msg = """В PennyJob можно зарабатывать ставя лайки, делая репосты и вступая в группы. Для работы Вам понадобится qiwi кошелек."""
    keyboard = keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Зарегистрировать на qiwi.com", url="https://qiwi.com/")
    keyboard.add(callback_button1)
    callback_button2 = types.InlineKeyboardButton(text="У меня уже есть qiwi кошелек", callback_data="alredy_have_qw")
    keyboard.add(callback_button2)
    bot.send_message(chat_id=chat_id, text=help_msg, reply_markup=keyboard)
    

@bot.callback_query_handler(func=lambda call:call.data == "alredy_have_qw")
def alredy_have_qw(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, text="Отлично! Нажмите /job, чтобы приступить.")
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
    bot.delete_message(chat_id, message_id=call.message.message_id)
    #bot.register_next_step_handler(call, delete_previous_inline_keyboard)

@bot.message_handler(commands=['job'])
def job_func(message):
    chat_id = message.chat.id
    #tl.del_msg(message)
    #check user:
    user_dict[chat_id] = {} #init user
    check_user = db.get_worker_info(chat_id)
    if check_user:
        user_dict[chat_id]["qw"] = check_user["qiwi_wallet"]
        user_dict[chat_id]["vk"] = check_user["vk_id"]
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        itembtn1 = types.KeyboardButton('Поставить лайк')
#         itembtn2 = types.KeyboardButton('Сделать репост')
#         itembtn3 = types.KeyboardButton('Вступить в группу')
        markup.add(itembtn1)
        bot.send_message(chat_id, "Вот, какие задания у меня есть для тебя:", reply_markup=markup)
        bot.register_next_step_handler(message, select_task_type)
    else:
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Регистрация", callback_data="user_registration")
        keyboard.add(callback_button)
        try:
            print(message.message_id, message.text)
            bot.send_message(chat_id, "Похоже, Вы не зарегистрированы.", reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(chat_id, "Регистрация не займет много времени :)", reply_markup=keyboard)
        except:
            bot.send_message(chat_id, "Похоже, Вы у нас впервые. Регистрация не займет много времени :)", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data=="user_registration")
def user_reg_call(call):
    chat_id = call.message.chat.id
    print(call.message.message_id)
    try:
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id-1)
        #bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    except:
        pass
    try:
        bot.send_message(chat_id, text = "Регистрация...")
        check_user = db.get_worker_info(chat_id)
        user_dict[chat_id]["qw"] = None
        user_dict[chat_id]["vk"] = None
        if check_user:
            bot.send_message(chat_id, text="Вы уже зарегистрированы. Нажмите /job, чтобы приступить к заданиям.")
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
            bot.delete_message(chat_id, message_id=call.message.message_id)

        else:
            chat_id = call.message.chat.id
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id)
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            registration_new_user(call.message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id, text=hello_msg)

def select_task_type(message):
    type_ = message.text
    chat_id = message.chat.id
    if type_ == 'Поставить лайк':
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Готово", callback_data="check_likes")
        keyboard.add(button)
        bot.send_message(chat_id, text="https://vk.com/qiwirussia?w=wall-13883743_607162")
        bot.send_message(chat_id, text="Перейдите по ссылке выше и поставьте лайк. Когда закончите, нажмите кнопку 'Готово'.", reply_markup=keyboard)

#     elif type_ == 'Сделать репост':
#         bot.send_message(chat_id, text="Хуй тебе, а не репост!")
#     elif type_ == 'Вступить в группу':
#         bot.send_message(chat_id, text="У меня лучше идея! Пойди-ка на хуй! Ура.")



@bot.callback_query_handler(func=lambda call: call.data=="check_likes")
def check_likes(call):
    chat_id = call.message.chat.id
    if db.get_task_user(chat_id):
        bot.send_message(chat_id, text="Извините, Вы уже выполнили это задание.")
    else:              
        try:
            if vk.is_user_liked_post("https://vk.com/qiwirussia?w=wall-13883743_607162", user_dict[chat_id]["vk"]):
                if qw.send_p2p(qiwi_token, to_qw=user_dict[chat_id]["qw"], sum_p2p=1, comment=str(chat_id)) == "OK":
                    if db.assign_task_to_user(chat_id):
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Успешно!")
                else:
                    bot.send_message(chat_id, text="Не мОжу провести платеж")
            else:
                bot.send_message(chat_id, text="Извините, но похоже Вы не поставили лайк.")
        except Exception as e:
            print(e)
            bot.send_message(chat_id, text=hello_msg)

def registration_new_user(message):
    chat_id = message.chat.id
    check_user = db.get_worker_info(chat_id)
    if user_dict[chat_id]["qw"] == None:
        msg_get_qw(message)
    elif user_dict[chat_id]["vk"] == None:
        msg_get_vk(message)  
    else:
        db.insert_worker(user_id=chat_id, qiwi_wallet = user_dict[chat_id]["qw"], vk_id=user_dict[chat_id]["vk"])
        bot.send_message(chat_id=chat_id, text="Регистрация успешно завершена! Нажмите /job, чтобы приступить к заданиям.")
        #msg_success_registration(message)
        
def msg_get_qw(message):
    chat_id = message.chat.id
    tl.del_msg(message)
    keyboard = types.ReplyKeyboardMarkup(selective=False, one_time_keyboard=True, row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton("Номера qiwi кошелька совпадает с номером телефона", request_contact=True)
    button2 = types.KeyboardButton("Ввести номер qiwi кошелька вручную")
    keyboard.add(button1, button2)
    bot.send_message(chat_id, "Выберите один из вариантов", reply_markup=keyboard, )
    bot.register_next_step_handler(message, get_qw)

def get_qw(message):
    chat_id = message.chat.id
    try:
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    except:
        pass
    if tl.check_message(message):
        try:
            user_dict[chat_id]["qw"] = message.contact.phone_number
            registration_new_user(message)
        except:
            markup = types.ForceReply(selective=False)
            bot.send_message(chat_id, "Введите номер qiwi-кошелька в формате 79XXXXXXXXX", reply_markup=markup, )
            bot.register_next_step_handler(message, get_qw_text)
    else:
        try:
            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        except:
            pass

def get_qw_text(message):
    chat_id = message.chat.id
    try:
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    except:
        pass
    if tl.check_message(message):
        user_dict[chat_id]["qw"] = message.text
        registration_new_user(message)
    else:
        try:
            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        except:
            pass    

def msg_get_vk(message):
    chat_id = message.chat.id
    tl.del_msg(message)
    markup = types.ForceReply(selective=False)
    bot.send_message(chat_id, "Введите ваш ID в контакте", reply_markup=markup)
    bot.register_next_step_handler(message, get_vk)        

def get_vk(message):
    chat_id = message.chat.id
    try:
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    except:
        pass
    if tl.check_message(message):
        user_dict[chat_id]["vk"] = message.text
        registration_new_user(message)
    else:
        try:
            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        except:
            pass

bot.polling()