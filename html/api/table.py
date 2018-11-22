#!/usr/bin/python
import sys
import pandas as pd
sys.path.insert(0, '/var/www/cgi-bin')
import model as md
import cgi, os
import cgitb; cgitb.enable()

fs = cgi.FieldStorage()

string = ""

try:
    if not fs:
        # get request without specifying table name
        # return current table
        string = md.read_table().to_csv(index= False)
        print ("Content-Type: text/csv\n")
    else:
        # get request with table name
        # return asked table
        if 'table' in fs:
            string = md.read_table_given(fs['table'].value).to_csv(index= False)
            print ("Content-Type: text/csv\n")
        # post request
        # need to upload table
        # first check whether there are necessary files
        elif 'uname' not in fs:
            print ('Status: 400 Bad Request\r\n\r\n')
            string = 'If you are uploading table, please specify table name in \'uname\'.'
        elif 'filename1' not in fs:
            print ('Status: 400 Bad Request\r\n\r\n')
            string = 'If you are uploading table, please specify tablename1.'
        elif 'filename2' not in fs:
            print ('Status: 400 Bad Request\r\n\r\n')
            string = 'If you are uploading table, please specify tablename2.'
        elif 'filename3' not in fs:
            print ('Status: 400 Bad Request\r\n\r\n')
            string = 'If you are uploading table, please specify tablename3.'
        # all required data is provided
        # generate tuple pages and upload table
        else:
            fileitem1 = fs['filename1']
            fileitem2 = fs['filename2']
            fileitem3 = fs['filename3']
            tablen = fs['uname'].value
            md.generate_tuplepage(fileitem1,fileitem2,fileitem3)
            fileitem3.file.seek(0)
            md.upload_table(tablen,fileitem3)
except Exception as e:
    # unexpected error
    print ('Status: 500 Internal Server Error\r\n\r\n')
    print (str(e))
else:
    print (string)
