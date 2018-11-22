#!/usr/bin/python
import cgi
import json
import datetime
import model as md
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
tablen = form['tablename'].value
md.save_table(tablen)

print ("""Content-Type: application/json\n
""")

# Return a result
t = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
result = json.dumps({'status': 'OK', 'Time': t}, indent=1)

print(result)
print("\n")
