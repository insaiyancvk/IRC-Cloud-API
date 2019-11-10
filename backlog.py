#work under progress
import requests
import json
from collections import deque

streamURL = 'https://www.irccloud.com/chat/stream'

cookies = {'session':'8.eed80421609502e038cd384e3c254a77'}

stream = requests.get('https://www.irccloud.com/chat/stream', cookies = cookies,stream=True)

for line in stream.iter_lines():
    message = json.loads(line.decode('utf-8'))
    if message['type']== 'oob_include':
        daBacklog = requests.get('https://www.irccloud.com'+message['url'],cookies=cookies)
        daBackloginJSON = daBacklog.json()
        break

print(daBackloginJSON)