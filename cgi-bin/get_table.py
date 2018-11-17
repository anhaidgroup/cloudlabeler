#!/usr/bin/python
import cgi
import model as md
import json

fs = cgi.FieldStorage()

print """Content-Type: application/json\n
"""

d = md.read_data()
result = json.dumps(d, indent=1)

print(result)
print("\n")
