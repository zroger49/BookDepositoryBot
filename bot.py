"""Bot handling""" 

#Telegram web API bot
import telebot


#General libraries 
import time 


#Import code from project
from bot_function import * 

#import cost
from const import BOT_TOKEN


def run_bot(): 
    bot = telebot.TeleBot(BOT_TOKEN) 

    @bot.message_handler(commads=['start'])
    def handle_start_comand(message): 
        while (True):         
            bot.reply_to(message, format_book_list(get_book_list()))
            time.sleep(86400)

    @bot.message_handler(commands=['wishlist'])
    def handle_wishlist_command(message):
        bot.reply_to(message, format_book_list(get_book_list()))
    
    bot.polling()
