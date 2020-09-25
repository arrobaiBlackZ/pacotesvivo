import os
import json

from settings import cookies_path 

with open(cookies_path, 'r') as file_object:
	file_content = file_object.read()
	dict_cookies = json.loads(file_content)
	