#!/usr/bin/env python
# __author__ = 'vagelim'

import gspread_utils as gs  # Testing
from config import DEFAULT_NUMBER, SHARE_EMAIL
from sms import sendTxt

############
# KEYWORDS #
############
ADMIN = '!'  # Admin command prefix
EXPENSE = '@'  # For expense tracking
NEW_USER = 'add'  # New user keyword


def interpreter(content=None):
    """Takes a message object, containing: msisdn, recipient, message, id, timestamp"""
    if content is None or content['message'] == '':
        return 0

    print content['message']  # Debugging

    # Add 1 to the front of the phone number (Nexmo requires it for sending SMS)
    # Makes this app USA only for the moment :(
    if content['msisdn'][0] != '1':
        # Append it
        l = []
        l.append('1')
        l.append(content['msisdn'])
        content['msisdn'] = ''.join(l)

    # Message contains administrative commands
    if ADMIN is content['message'][0]:
        pass

    # If it is a request from a user to add themselves
    if NEW_USER == content['message'].lower():
        gs.addUser(content['msisdn'])

    # Message contains expenses
    elif EXPENSE is content['message'][0]:
        # Clean the timestamp
        content['timestamp'] = content['timestamp'].split()[0]
        # Clean and normalize the message
        content['message'] = content['message'][1:].lower()

        # Get user workbook
        book = gs.getUserBook(content['msisdn'])

        if book != -1:  # Book == -1 if user does not exist
            sheet = gs.getSheet(content['timestamp'], book)
            result = gs.commit(content, sheet)
            if 'malformed' == result:
                sendTxt(
                    "New users, txt: 'add'\nAdd expense format:\n@<category>:cost <category>:cost", content['msisdn'])

    # If the message is a URL, assume the user is trying to add themselves
    # to the system. This also allows for updating one's workbook on the fly.
    elif 'http' == content['message'][:4]:
        gs.addUser(content['msisdn'], content['message'])
        sendTxt("Workbook added!\n Make sure you share it with " + SHARE_EMAIL, content['msisdn'])

if __name__ == '__main__':  # For testing, should never run as main()
    import sys
    try:
        interpreter(sys.argv[1])
    except IndexError:
        content = {'msisdn': DEFAULT_NUMBER, 'message': "@Food:10",
                   'recipient': DEFAULT_NUMBER, 'timestamp': '2015-11-23 none'}
        content['message'] = raw_input("Command to run: ")
        interpreter(content)
    exit()
    