import requests
import re
import os
from twilio.rest import Client
from bs4 import BeautifulSoup
from setting import *


class book_info:
    def __init__(self, wish_list_item):
        self.wish_list_item = wish_list_item

    def get_item_info(self):
        """Parse information about the book from HTML"""
        self.title = (
            self.wish_list_item.find("div", class_="item-info")
            .h3.a.text.strip("\n")
            .strip()
        )
        try:
            # book that are not avaiable do not have a price
            self.current_price = (
                self.wish_list_item.find("div", class_="price-wrap")
                .p.text.split("€")[0]
                .strip("\n")
                .strip()
            )
        except AttributeError:
            self.current_price = "Book out of stock"
            self.raw_price = "Book out of stock"
            self.discount = 0
            return
        try:
            # Some books do not have discount
            self.discount = (
                self.wish_list_item.find("div", class_="savings-splat")
                .text.strip("\n")
                .strip()
                .strip("%off")
            )
        except AttributeError:
            self.discount = "0"
        try:
            # As some books do not have discount this atribute does not exist
            self.raw_price = self.wish_list_item.find(
                "div", class_="price-wrap"
            ).p.span.text.strip(" €")
        except AttributeError:
            self.raw_price = self.current_price


def verify_homepage(soup):
    """verify the wishlist code (wrong wishlist codes redirect to homepage)"""
    testing = soup.find_all(
        "div", class_="tab-wrap module type-paragraph grid tab-3771 tab-active"
    )  # This class does not appear in wishlist
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


def main():
    wishlist = requests.get(
        "https://www.bookdepository.com/wishlists/{}".format(wish_list_code)
    )
    soup = BeautifulSoup(wishlist.content, "html.parser")
    if not verify_homepage(soup):
        raise Exception("Error: invalid wishlist code")

    book_list = []
    wish_list_len = get_wish_list_len(soup)
    for page_number in range(1, wish_list_len + 1):
        if page_number == 1:
            pass
        else:
            # updates wishlist link
            wishlist = requests.get(
                "https://www.bookdepository.com/wishlists/{}?page={}".format(
                    wish_list_code, page_number
                )
            )
            print(
                "https://www.bookdepository.com/wishlists/{}?page={}".format(
                    wish_list_code, page_number
                )
            )
            soup = BeautifulSoup(wishlist.content, "html.parser")
        # gets all books in the page
        wish_list_items = soup.find_all("div", class_="book-item")
        for item in wish_list_items:
            book = book_info(item)
            book.get_item_info()
            book_list.append(book)

    ###Get the text for each book
    sender_text = ""
    list_of_texts = []
    for wish_book in book_list:
        putative_sender_text = f"{wish_book.title}\nPrice: {wish_book.current_price}€\nDiscount: {wish_book.discount}% \n\n"
        if len(sender_text) + len(putative_sender_text) > 1600:
            list_of_texts.append(sender_text)
            sender_text = putative_sender_text
        else:
            sender_text += putative_sender_text
    list_of_texts.append(sender_text)

    for sender_text in list_of_texts:
        # send message to whatapp
        client = Client(
            "AC564a02ce7f16495f81ade0935b2f9192", "3bc0da3ef646abec902771448305fd1a"
        )
        message = client.messages.create(
            body=sender_text, from_="whatsapp:p+14155238886", to=phone
        )


if __name__ == "__main__":
    main()
