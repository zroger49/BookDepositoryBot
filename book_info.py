"""Class for holding and parsing information about each book"""

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


