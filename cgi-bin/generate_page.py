#!/usr/bin/python
import cgi, os
import cgitb; cgitb.enable()
import sqlite3
import model as md
import traceback

form = cgi.FieldStorage()
# Get filename here.
fileitem1 = form['filename1']
fileitem2 = form['filename2']
fileitem3 = form['filename3']
tablen = form['uname'].value

#Test if the file was uploaded
if fileitem1.filename and fileitem2.filename and fileitem3.filename:
   try:
       html = md.generate_tuplepage(fileitem1,fileitem2,fileitem3)
       fileitem3.file.seek(0)
       md.upload_table(tablen,fileitem3)

       message = "<p><font size=\"6\"><b>Your table has been successfully uploaded!</b></font></p>"
       message = message + "<p>To load your new table, enter your new table's name and click load.</p>"
       message = message + "<p><strong>Note:</strong> Save your old table before loading your new table or the data will be lost.</p>"
       message = message + "<p>Below is a preview of one tuple pair page:</p>"
       message = message + html
   except Exception,e:
       message = "<p><font size=\"6\"><b>An error has occured!</b></font></p>"
       message = message + "<p>Please check your csv files according to the error message!</p>"
       message = message + "<p>Key Word for the error is: " + str(e) + "</p>"
       message = message + "<p>Detailed traceback: </p><p>" + traceback.format_exc() + "</p>"

else:
   message = 'Please choose three CSV files'


print """\
Content-Type: text/html\n
<html>
<body>
   <p>%s</p>
</body>
</html>
""" % (message,)
