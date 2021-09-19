"""Entry point for the BookDepositoryBot"""

from bot import BookDepositoryBot
from const import BOT_TOKEN


if __name__ == "__main__": 
    bot = BookDepositoryBot(BOT_TOKEN)
    bot.run()