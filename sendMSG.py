 
import requests
import json
from collections import deque

def getCID(sessionID):

    streamURL = 'https://www.irccloud.com/chat/stream'

    cookies = {'session': sessionID}

    stream = requests.get('https://www.irccloud.com/chat/stream', cookies = cookies,stream=True)

    for line in stream.iter_lines():

        message = json.loads(line.decode('utf-8'))

        if message['type']== 'oob_include':

            daBacklog = requests.get('https://www.irccloud.com'+message['url'],cookies=cookies)
            
            daBackloginJSON = daBacklog.json()
            
            break

    for event in daBackloginJSON:

        if event['type']=='makeserver':
            
            cid = event['cid']
    
    return cid


def getToken():

    r = requests.post("https://www.irccloud.com/chcvat/auth-formtoken").json()

    token = r['token']
    
    return token

def getSessionID(email,password,token):
    loginURL = "https://www.irccloud.com/chat/login"

    data = {
    'email': email,
    'password': password,
    'token':token
    }

    headers = {
        'content-type':'application/x-www-form-urlencoded',
        'x-auth-formtoken':token
        }
    auth = requests.post(loginURL,data = data, headers = headers).json()   
    
    if auth['success'] == True:
        session = auth['session']
        return session
    else:
        return False

def sendMessage(uname,session,cid,msg):

    dataSendMessage = {
        "msg":"/msg "+uname+" "+msg,
        "to":"*",
        "cid":cid,
        "session":session
    }

    sendMsgURL = "https://www.irccloud.com/chat/say"

    cookies = {'session':session}

    sendMsg = requests.post(sendMsgURL,data = dataSendMessage, cookies = cookies).json()
    
    if sendMsg['success'] == True:
        return True
    else:
        return sendMsg

def main():
    token = getToken()
    email=input("Enter the email id and password to log in : ")
    
    password = input("Password: ")

    sessionID = getSessionID(email,password,token)

    cid = getCID(sessionID)

    if sessionID!=False:

        msg = input("Enter the message : ")
        
        uname = input("Enter the nick of the receiver : ")

        response = sendMessage(uname,sessionID,cid,msg)

        if response!=True:
            print(response)
    
    else:
        print("Authentication Failed")

main()
