#!/usr/bin/env python
# __author__ = 'vageli'

import cgi, cgitb
import sys

from sms import sendTxt
from interpreter import interpreter

print "Content-type:text/html\r\n\r\n"
print 'HTTP/1.1 200 OK\r\n\r\n'

#Get all fields
form = cgi.FieldStorage() 
msisdn = form.getvalue('msisdn')
to  = form.getvalue('to')
messageId = form.getvalue('messageId')
text  = form.getvalue('text')
message_timestamp = form.getvalue('message-timestamp')
type  = form.getvalue('type')
msisdn = str(msisdn)
msisdn = msisdn.translate(None, "'")
to = str(to)
to = to.translate(None, "'")
messageId = str(messageId)
messageId = messageId.translate(None, "'")
text = str(text)
text = text.translate(None, "'")
message_timestamp = str(message_timestamp)
message_timestamp = message_timestamp.translate(None, "'")
type = str(type)
type = type.translate(None, "'")

print "<html>"
print "<head>"
print "<title>Test Callback</title>"
print "</head>"
print "<body>"
print "<h2>MSISDN: %s \r\nTo:%s \r\nmessageId: %s \r\nText: %s\r \nTimestamp: %s \r\nType %s</h2>" % (msisdn, to, messageId,text,message_timestamp,type)
print "</body>"
print "</html>"

#Build an object with all message details
content = {'msisdn' : msisdn, 'recipient' : to , 'id' : messageId , 'message' : text , 'timestamp'  : message_timestamp}

message = 'MSISDN: ' + msisdn + '\nTo: ' + to + '\nmessageId: ' + messageId + '\nTEXT:' + text + '\n\nTimestamp: ' + message_timestamp



interpreter(content)
