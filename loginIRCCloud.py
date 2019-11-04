import requests

r = requests.post("https://www.irccloud.com/chat/auth-formtoken").json()

token = r['token']

print(token)

loginURL = "https://www.irccloud.com/chat/login"

data = {
    'email':'cvamshik1@gmail.com',
    'password':'CVKvamsi111!',
    'token':token
    }

headers = {
    'content-type':'application/x-www-form-urlencoded',
    'x-auth-formtoken':token
    }

auth = requests.post(loginURL,data = data, headers = headers).json()

session = auth['session']
print(session)

cid = 1029767

dataSendMessage = {
    "msg":"/msg akshay from the script.",
    "to":"*",
    "cid":cid,
    "session":session
}

sendMsgURL = "https://www.irccloud.com/chat/say"

cookies = {'session':session}

sendMsg = requests.post(sendMsgURL,data = dataSendMessage, cookies = cookies).json()

print(sendMsg)