import requests
import json
from collections import deque

neid=0
cid = 0

def getCID(sessionID):

    global neid,cid
    eid = 0

    streamURL = 'https://www.irccloud.com/chat/stream'

    cookies = {'session':sessionID}

    stream = requests.get('https://www.irccloud.com/chat/stream', cookies = cookies,stream=True)

    for line in stream.iter_lines():

        message = json.loads(line.decode('utf-8'))

        if message['type']=='stat_user':

            bufferID = message['last_selected_bid']

        elif message['type']== 'oob_include':

            url = message['url']

            daBacklog = requests.get('https://www.irccloud.com'+message['url'],cookies=cookies)

            daBackloginJSON = daBacklog.json()
            
            break
    
    
    
    file1 = open("deBacklog.txt","w")
    file1.write(daBacklog.text)
    file1.close()

    for event in daBackloginJSON:

        if event['type']=='makeserver':
            
            cid = event['cid']
        
        elif event['bid']==bufferID and event['type']=='buffer_msg':
                bid = event['bid']
                eid = event['eid']

    for event in daBackloginJSON:

        if event['eid'] == eid and event['type'] == 'buffer_msg':
            msg = event['msg']
            if neid!=eid:
                neid=eid
                print(msg,bufferID)
            getCID(sessionID)    


def getToken():

    r = requests.post("https://www.irccloud.com/chat/auth-formtoken").json()

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

def auth():

    token = getToken()
    email = input("Enter email id and password to log in :")
    password = input()
    sessionID = getSessionID(email,password,token)

    return sessionID


def main():

    sessionID = auth()
    global cid

    sessionID = '8.222e5f6e8e73257012ca773f369e276a'

    getCID(sessionID)

    if sessionID!=False:

        msg = input("Enter the message : ")
        
        uname = input("Enter the nick of the receiver : ")

        response = sendMessage(uname,sessionID,cid,msg)

        if response!=True:
            print(response)
    else:
        print("Authentication Failed")
main()
