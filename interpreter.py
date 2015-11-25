#!/usr/bin/env python
# __author__ = 'vagelim'

import subprocess
import requests

import gspread_utils as gs#Testing
from config import DEFAULT_NUMBER
############
# KEYWORDS #
############
EXPENSE = '@' #For expense tracking


def interpreter(content=None):
    """Takes a message object, containing: msisdn, recipient, message, id, timestamp"""
    if content == None:
        return 0

    if EXPENSE in content['message'][0] :
        #Clean the timestamp
        content['timestamp'] = content['timestamp'].split()[0]
        #Clean and normalize the message
        content['message'] = content['message'][1:].lower()

        sheet = gs.getSheet(content['timestamp'])
        gs.commit(content, sheet)


if __name__ == '__main__': #For testing, should never run as main()
    import sys
    try:
        interpreter(sys.argv[1])
    except IndexError:
        content = {'msisdn' : DEFAULT_NUMBER, 'message' : "@Food:10", 'recipient': DEFAULT_NUMBER, 'timestamp' : '2015-11-23 none'}
        content['message'] = raw_input("Command to run: ")
        interpreter(content)
    exit()