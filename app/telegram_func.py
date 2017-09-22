user_dict = {}
from telebot import types
import telebot
bot = telebot.TeleBot(token)
def reset_dict(user_id):
    user_dict[user_id] = {}
    user_dict[user_id]["type"] = None
    user_dict[user_id]["qw"] = None
    user_dict[user_id]["vk"] = None
    return user_dict
    
handler_names = ["/start", "/begin", "/job"]

def check_message(message):
	text = message.text
	if text in handler_names:
		return False
	else:
		return True

def del_msg(message):
    chat_id = message.chat.id
    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id)
    except:
        pass
    try:
        bot.delete_message(chat_id, message_id=message.message_id)
    except Exception as e:
        print(e)
        pass