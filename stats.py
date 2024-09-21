#!/usr/bin/env python3

import re
import urllib.request

MYSTATS="http://multirpg.net/rawplayers2.php"

# Read the data
with urllib.request.urlopen(MYSTATS) as response:
       html = response.read()

# Convert bytes to string
html=str(html, 'UTF8')
strings=html.split('\n')

print(strings[0])
