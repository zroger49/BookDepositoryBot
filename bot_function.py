"""General Function to be used by the bot itself"""


#General libraries
import re 

from bs4 import BeautifulSoup
import requests


from book_info import book_info
from const import WISH_LIST_CODE
from request import send_wishlist_request

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
    wishlist = send_wishlist_request(f"https://www.bookdepository.com/wishlists/{WISH_LIST_CODE}")
    if wishlist: 
        soup = BeautifulSoup(wishlist.content, "html.parser")
        if not verify_homepage(soup):
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
        if book.current_price == "Book out of stock": 
            text_to_send += f"{book.title}\n{book.current_price}\nDiscount: {book.discount}% \n\n"    
        else: 
            text_to_send += f"{book.title}\nPrice: {book.current_price}€\nDiscount: {book.discount}% \n\n"
    return text_to_send

