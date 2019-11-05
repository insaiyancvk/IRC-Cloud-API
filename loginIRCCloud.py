import requests

cid = 000000

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

def main():
    token = getToken()
    email=input("Enter the email id and password to log in : ")
    #email = 'xxxx'
    password = input("Password: ")
    #password = 'xxxx'

    sessionID = getSessionID(email,password,token)

    #print(sessionID,resp)

    if sessionID!=False:

        msg = input("Enter the message : ")
        
        uname = input("Enter the nick of the receiver : ")

        response = sendMessage(uname,sessionID,cid,msg)
    
    else:
        print("Authentication Failed")

main()
