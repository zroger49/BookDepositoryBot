"""Module that deals with the requests"""

import requests

def send_wishlist_request(url):
    try: 
        wishlist = requests.get(url)
        return wishlist
    except Exception as e:
        print("Request failed, error: " + str(e))