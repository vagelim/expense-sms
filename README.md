# Expense-SMS

### Description & Motivation
Expense-SMS is a python software package that enables you to keep track of your finances via SMS.  

I had been using Google Sheets by itself to track my spending habits, but found that if I didn't enter an expense immediately after it was incurred, it usually wouldn't make it into my sheet.

I had a shortcut on my phone which linked to my expense spreadsheet, but when opening it on Android (which is the device I most commonly use) I then had to open the sheet _yet again_ in the Google Sheets app. The whole experience took about a minute for something as simple as data entry. Way too long.

Enter **Expense-SMS**

Being obsessed with SMS as an interaction medium, I quickly saw the potential to SMS-ify my spreadsheet. Sending an SMS is quick, and bringing up my messaging app and firing off a txt takes less than 15 seconds. And if I'm away from my smartphone, I can even use a dumbphone to keep my sheet updated. 

Leveraging my existing experience with Nexmo and its API, the next step was learning to use gspread and the rest is history.


## Requirements

#### Python Dependencies
gspread, nexmo, oauth2client  
`pip install gspread nexmo oauth2client`

#### External services
- [Nexmo API keys](https://dashboard.nexmo.com/) - Click "Api Settings" in the upper right corner    
- Google Account  
- [OAuth2 Credentials for gspread](https://gspread.readthedocs.org/en/latest/oauth2.html)  
- A python-ready webserver  


## Initial Setup
1. [Clone the repo](https://github.com/vagelim/expense-sms.git) 
2. `chmod +x` the python files   
2. Modify `config.py`, change:  
    - `DEFAULT_NUMBER` to your phone number. This number is used for debugging purposes
    - `NEXMO_NUMBER` to the phone number in your Nexmo account
    - `NEXMO_API_KEY` to your Nexmo API key
    - `NEXMO_SECRET` to your Nexmo secret
    - `SHARE_EMAIL` to the `client_email` in your OAuth2 json file
    - `ADMIN_BOOK` to the URL of the Google Sheets workbook to use to store administrativia
    - `GCONF` to the location of your gspread OAuth2 credentials (recommend putting these in a location other than webserver root, i.e. **NOT** in `/var/www`). Remember to make these readable to your webserver user
    - `SELF_SERVICE` to `True` if you want users to be able to add themselves via txt message
3. Share the workbook at ADMIN_BOOK with the email in your OAuth2 credentials, listed as `client_email`.  
**Note**: You may receive a "Message Undeliverable" notice in your email after sharing. Ignore it.
4. Add your first user
    - Go to your `ADMIN_BOOK` and in the first column input your phone number (no spaces or dashes)
    - In the adjacent column, enter the Google Sheets URL of the workbook you want to track _your_ expenses in
    - **Make sure** the workbook is shared with the email defined in `SHARE_EMAIL`  
### Usage
Messages sent to Expense-SMS follow this format:  
`@<item>:<price>`  
So if I wanted to commit an expense of $10 for a movie, I'd send the following: `@Movie:10`  
Note that the item names are case insensitive, and will be casted to lowercase by default.  

You can also send more than one expense by separating with whitespace. Only one `@` symbol is needed, at the beginning.  
`@test:1 test2:2`  


Also works with negative numbers, so if you want to add income, you would send it as a negative value (somewhat counter-intuitive, but this was meant to track expenses, not income).  
`@check1:-30`  


### Customization
Right now, you can customize the character identifier, currently set to the `@` symbol. To change it, modify the `EXPENSE` variable in `interpreter.py`.  



### The Road Ahead
- The _magic cell_ `D1` in each sheet acts as a running tally of that day's expenses. I plan to soon implement a feature that will create a sheet that displays total monthly expenses, broken down by category.

    To do that will require going through all sheets in a month (2015-11-*, for example), making a set containing all item names, and updating the cost associated with each name, with information from all sheets from that month.

- Implementing functionality to query the workbook.  
        Because Nexmo does not charge for incoming messages, and because I want to commit expenses more often than I want to look at them, this feature is not of immediate neccessity (in my use case).

- Per-user settings  
  Users should be able to configure their own _magic cells_ and any other settings that may be added in the future

- Move all possible configuration options into `ADMIN_BOOK`

#Try it out yourself!
You can try it out yourself today! Get started by txting `add` to **12242028246**.  
Then, follow the prompts.  
Make sure the Google Sheets URL you send is shared with: `account-1@genial-aspect-113800.iam.gserviceaccount.com`
