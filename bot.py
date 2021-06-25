#General libraries
import re 
import time
from icecream import ic 

#Webparsing libraries
from bs4 import BeautifulSoup
import requests

#Telegram web API bot
import telebot

#book class
from book_info import book_info

from const import BOT_TOKEN, WISH_LIST_CODE


def verify_homepage(soup):
    """verify the wishlist code (wrong wishlist codes redirect to homepage)"""
    testing = soup.find_all(
        "div", class_="tab-wrap module type-paragraph grid tab-3771 tab-active"
    )  # This class does not appear in wishlist but appears in the homepage
    if testing == []:
        return True  # return true if the webpage is not the homepage
    else:
        return False


def get_wish_list_len(soup):
    """Get the lenght of pages in the wishlist (number of URL's)"""
    wish_list_right = soup.find(
        "ul", class_="pagination pagination-sm responsive-pagination"
    )
    try:
        inter = str(wish_list_right.contents[-4])
    except AttributeError:
        # Attribute Error arises probably from missing pagination on the rights, which means the wishlist only has 1 page
        return 1
    re_search = re.search("page=([0-9]+)", inter)
    return int(re_search.group(1))


def get_book_list():
    """Store information about the books in a list"""
    wishlist = requests.get(
        f"https://www.bookdepository.com/wishlists/{WISH_LIST_CODE}"
    )
    soup = BeautifulSoup(wishlist.content, "html.parser")
    if not verify_homepage(soup):
        ic(soup)
        raise Exception("Error: invalid wishlist code")

    book_list = []
    wish_list_len = get_wish_list_len(soup)
    for page_number in range(1, wish_list_len + 1): #Loops through the wishlist pages
        if page_number != 1:
            # updates wishlist link for i != 1
            wishlist = requests.get(f"https://www.bookdepository.com/wishlists/{WISH_LIST_CODE}?page={page_number}")
            soup = BeautifulSoup(wishlist.content, "html.parser")
        # gets all books in the page
        wish_list_items = soup.find_all("div", class_="book-item")
        for item in wish_list_items:
            book = book_info(item)
            book.get_item_info()
            book_list.append(book) #Add the information to the bookList
    
    return book_list

def format_book_list(book_list):
    """Formats the list of books into a single string message to send """ 
    text_to_send = ""
    for book in book_list: 
        text_to_send += f"{book.title}\nPrice: {book.current_price}€\nDiscount: {book.discount}% \n\n"
    return text_to_send

def run_bot(): 
    bot = telebot.TeleBot(BOT_TOKEN) 

    @bot.message_handler(commands=['start'])
    def handle_start_comand(message): 
        while (True): 
            time.sleep(86400)        
            bot.reply_to(message, format_book_list(get_book_list()))

    @bot.message_handler(commands=['wishlist'])
    def handle_wishlist_command(message):
        bot.reply_to(message, format_book_list(get_book_list()))
    
    bot.polling()


run_bot() 
