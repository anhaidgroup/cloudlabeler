#!/usr/bin/python
import cgi
import model as md
import json
import datetime
import os

fs = cgi.FieldStorage()

print """Content-Type: application/json\n
"""

label_info = fs.getvalue('checked_options')
md.save_data(label_info)
t = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
result = json.dumps({'status': 'OK', 'Time': t}, indent=1)

print(result)
print("\n")
