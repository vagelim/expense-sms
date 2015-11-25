#!/usr/bin/env python
# __author__ = 'vagelim'
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

from config import SHEETS_URL, GCONF


def getWorkbook(url=SHEETS_URL):

    json_key = json.load(open(GCONF))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    gc = gspread.authorize(credentials)

    book = gc.open_by_url(url)

    return book

def getSheet(sheet):
    """Takes a sheet name and book, returns the sheet
    If called without a book, gets the default"""
    book=getWorkbook() 

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

def getValue(sheet, book=getWorkbook() ):
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
            sheet.update_cell(depth, 2 , price)


