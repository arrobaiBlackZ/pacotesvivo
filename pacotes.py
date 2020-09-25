import os
import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from http_clients import client
from settings import allowed_cookies, data, cookies_path
from files import dict_cookies
from utils import humanbytes

client.headers.update({
	'User-Agent': input('Digite seu agente de usuário: ')
})

for cookie in dict_cookies:
	if cookie['name'] in allowed_cookies:
		cookies = {'JSESSIONID': cookie['value']}
		client.cookies.update(cookies)
		break

response = client.post('contrataPacote.do', data=data, cookies=cookies)
if response.status_code == 200:
	json_response = response.json()
elif response.status_code == 404:
	raise ValueError('O agente de usuário inserido é inválido.')

if not json_response['isContratado']:
	raise ValueError('Não é possível realizar contratações de pacotes para esta linha neste momento.')
else:
	bytes = 419430400
	pacotes = 1

while json_response['isContratado']:
	
	try:
		response = client.post('contrataPacote.do', data=data, cookies=cookies)
	except Exception:
		pass
	finally:
		json_response = response.json()
		if json_response['isContratado']:
			bytes = bytes + 419430400
			pacotes = pacotes + 1
			json_dump = json.dumps(json_response, indent=4, sort_keys=True)
			print(
				highlight(json_dump, JsonLexer(), TerminalFormatter())
			)

total = humanbytes(bytes)

print(
	f'Pacotes contratados: {pacotes}\nTotal de internet: {total}\nValidade: 7 dias.'
)

os.remove(cookies_path)

quit()
