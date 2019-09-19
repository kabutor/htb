from mitmproxy import http, ctx
import requests, regex

def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == "POST":
        token = flow.request.urlencoded_form["token"]
        cookie = flow.request.headers["Cookie"]
        #real_post = form.get_first("token")
        #Log para debug
        #ctx.log.info("Cookie " + cookie)
        ctx.log.info("token " + token)
         
        r = requests.get("http://10.10.10.129")

        new_cookie = (r.cookies['PHPSESSID'])
        new_token = (regex.search('token\" value=\"\K.{64}',r.text)).group()

        flow.request.headers["Cookie"] = flow.request.headers["Cookie"].replace("12345", new_cookie)
        flow.request.urlencoded_form["token"] = token.replace("abcdef", new_token)
