#!/usr/bin/python
import cgi
import model as md
import json
import os

fs = cgi.FieldStorage()

print ("""Content-Type: application/json\n
""")

checked_data = fs.getvalue('checked_options')
d = md.read_data(filter_label_str=checked_data)
result = json.dumps(d)

print(result)
print("\n")
