# __author__ = 'vagelim'
#Authentication and configuration


AUTHORIZED_NUMBERS = ['', ''] #Authorized phone numbers
DEFAULT_NUMBER = '' #Number to send debug messages to 
NEXMO_NUMBER = ''


NEXMO_API_KEY  = '' 
NEXMO_SECRET = '' 

#GSPREAD
SHEETS_URL = 'https://docs.google.com/spreadsheets/d/really-long-UUID/edit#gid=0'

GCONF = ''
#Remember, SHEETS_URL must end with "edit#gid=0" and MUST be shared with "client_email" from json file
#In our case, must be shared with: account-1@conspicuous-interface-113300.iam.gserviceaccount.com


#Control characters and keywords for the command interpreter are in interpreter.py