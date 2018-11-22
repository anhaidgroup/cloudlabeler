#!/usr/bin/python
import sys
sys.path.insert(0, '/var/www/cgi-bin')
import model as md
import cgi, os
import cgitb; cgitb.enable()

fs = cgi.FieldStorage()

string = ""

try:
    if 'table' not in fs:
        # get request without specifying table name
        # return current summary
        string = md.get_summary(api=True)
        print ("Content-Type: text/json\n")
    else:
        # get request with table name
        # return asked table
        string = md.get_summary(fs['table'].value,api=True)
        print ("Content-Type: text/json\n")
except Exception as e:
    # unexpected error
    print ('Status: 500 Internal Server Error\r\n\r\n')
    print (str(e))
else:
    print (string)
