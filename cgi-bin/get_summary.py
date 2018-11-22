#!/usr/bin/python
import cgi
import model as md
import json

fs = cgi.FieldStorage()

print ("""Content-Type: application/json\n
""")

l = md.get_summary()
result = json.dumps(l, indent=1)

print(result)
print("\n")
