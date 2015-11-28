# __author__ = 'vagelim'
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

from config import GCONF, ADMIN_BOOK, SELF_SERVICE, SHARE_EMAIL
from sms import sendTxt #Be able to send SMS

def getWorkbook(url):
    json_key = json.load(open(GCONF))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    gc = gspread.authorize(credentials)

    book = gc.open_by_url(url)

    return book

def getSheet(sheet, book):
    """Takes a sheet name and book, returns the sheet"""


    list_sheets = book.worksheets()
    #Check to see if the sheet exists
    if sheet in str(list_sheets):
        #It does, use it
        sheet = book.worksheet(sheet)

    #If not, create and use it
    else:
        sheet = book.add_worksheet(title=sheet, rows="100", cols="20")
        #Create the 'magic cell'
        #The magic cell is the total of all expenses

        sheet.update_acell('D1', '=SUM(B1:B100)')

    return sheet

def getValue(cell, sheet, book=None ):
    pass

def commit(content, sheet):
    """Takes a message object and writes expenses to a spreadsheet"""
    #Get the date of the message, to determine which spreadsheet to use
    date = content['timestamp']

    #Unpack the content
    #Expenses follow the format: <NAME>:cost with spaces to separate multiple values
    #Example: Food:10 drink:20 movie:15

    col_values = sheet.col_values(1) #First column lists item, adjacent column lists price
    costs = content['message'].split(' ') 
    number = len(costs)


    for each in costs: # NAME IS CASESENSITIVE
        name, price = each.split(':')

        #Check if the item exists already
        if name in col_values: #If it does, add to that
            cell = sheet.find(name)
            new_col = cell.col + 1

            current_val = sheet.cell(cell.row, new_col).numeric_value

            if current_val == None:
                current_val = float(price)

            else:
                current_val += float(price)

            sheet.update_cell(cell.row, new_col, current_val) 
            #TODO check updated value

        #The item does not exist
        else:
            #Find the cardinality of the last element in col
            depth  = len(sheet.col_values(1))
            depth += 1
            sheet.update_cell(depth, 1 , name) #Append name to the last row, first column
            sheet.update_cell(depth, 2 , price) #Append price to the last row, second column

def getUserBook(phone_number):
    """Takes a phone number, returns phone number's workbook"""
    #Get Admin workbook
    book = getWorkbook(ADMIN_BOOK)

    #Get user sheet
    sheet = getSheet("users", book)

    #Check if phone_number is a valid user
    col_values = sheet.col_values(1) #First column lists users, second column is workbook URL
    if phone_number in col_values:
        cell = sheet.find(phone_number)
        #URL is adjacent column
        URL = sheet.cell(cell.row, cell.col + 1).value

        if URL[:4] == 'http': #If 'valid' URL
            try:
                book = getWorkbook(URL)

            except gspread.exceptions.SpreadsheetNotFound: #Workbook is not shared
                sendTxt('Workbook not found. Make sure you shared it with: ' + SHARE_EMAIL, phone_number)
                return -1
            except gspread.exceptions.NoValidUrlKeyFound: #Workbook URL is invalid
                return -1
                addUser(phone_number, URL='invalid')
            
            return book

        elif URL == '': #Field is empty
            pass

    else: #If not an existing user
        addUser(phone_number)
        return -1

def addUser(phone_number , URL=None):

    if SELF_SERVICE == False: #Users must be manually added
        return -1

    if URL == None:
        sendTxt("User not found. Please reply with a Google Sheets URL.", phone_number)

    if URL == 'invalid': #URL was invalid, user needs to make a new one
        sendTxt("Workbook is invalid. Please reply with a valid Google Sheets URL.", phone_number)
    #Get Admin workbook
    book = getWorkbook(ADMIN_BOOK)

    #Get user sheet
    sheet = getSheet("users", book)

    #Check if phone number has tried to add itself already
    col_values = sheet.col_values(1) #First column lists users, second column is workbook URL
    if phone_number in col_values:
        cell = sheet.find(phone_number)
        #Update the URL of the user's book
        sheet.update_cell(cell.row, cell.col + 1, URL)

    else: #The user just got sent a message telling them to add the URL
        #Add them to the db, so they will be recognized when they respond
        depth = len(sheet.col_values(1)) + 1
        sheet.update_cell(depth, 1, phone_number)

