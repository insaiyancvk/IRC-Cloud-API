import requests

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


def main():
    token = getToken()
    email=input("Enter the email id and password to log in : ")
    #email = 'xxxx'
    password = input("Password: ")
    #password = 'xxxx'

    sessionID = getSessionID(email,password,token)

    #print(sessionID,resp)

    if sessionID==False:
    
        print("Authentication Failed")

main()
