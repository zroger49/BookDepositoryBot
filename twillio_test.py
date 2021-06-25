import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
client = Client('AC564a02ce7f16495f81ade0935b2f9192', '3bc0da3ef646abec902771448305fd1a')

message = client.messages.create(
                              body='Hello there!',
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+351964076452'
                          )

print(message.sid)
