#!/usr/bin/env python
# __author__ = 'vagelim'
import nexmo

from config import DEFAULT_NUMBER, NEXMO_NUMBER, NEXMO_API_KEY, NEXMO_SECRET



def sendTxt(message, number=DEFAULT_NUMBER):

    client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_SECRET)
    t = client.send_message({'from': NEXMO_NUMBER, 'to': number, 'text': message})
    return t


if __name__ == '__main__': #For testing purposes only
    sendTxt('test from main', DEFAULT_NUMBER)
