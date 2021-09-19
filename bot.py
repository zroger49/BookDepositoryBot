"""Bot handling""" 

#Telegram web API bot
import telebot


#General libraries 
import time 


#Import code from project
from bot_function import * 

class BookDepositoryBot(): 
    def __init__(self, token) -> None:
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commads=['start'])
        def handle_start_comand(message): 
            while (True):         
                self.bot.reply_to(message, format_book_list(get_book_list()))
                time.sleep(86400)

        @self.bot.message_handler(commands=['wishlist'])
        def handle_wishlist_command(message):
            self.bot.reply_to(message, format_book_list(get_book_list()))

    def run(self): 
        self.bot.polling()
