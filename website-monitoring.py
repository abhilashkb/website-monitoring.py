import threading
import requests
import re
import json
from dns import resolver
webhook_url = 'https://hooks.slack.com/services/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'

with open('slackdata.txt') as slackd:
    slack_data = json.load(slackd)


with open('domains-list.txt') as domains:
    domain_list = domains.readlines()
with open('sites-down.txt') as down_sites:
    down_sitesl = [ x.strip() for x in down_sites.readlines()]
    

list_length= len(domain_list)

def status_code(domain):
    if re.match(r'\w+(\.\w+){1,3}$',domain):
        try:
            resolver.query(domain,'A')
            status_cod=str(requests.head('http://'+domain+'', headers={'User-Agent': 'Foo bar'},allow_redirects=True).status_code)
        except:
               status_cod='000'
        if re.match( r'[2,3]\d{2}$' ,status_cod.strip()):
            print("status ok")
            if domain in down_sitesl:
                print("resolved")
                slack_data['blocks'][0]['text']['text']=domain+' is up'
                response = requests.post(webhook_url, data=json.dumps(slack_data)
                ,headers={'Content-Type': 'application/json'})

                with open('site-down.txt','w') as down_list:
                    for d in down_sitesl:
                        if domain == d:
                            pass
                        else:
                            down_list.write(d)



        else:
            if domain not in down_sitesl:
                with open('sites-down.txt','a') as down_sites:
                    down_sites.write(domain)
                slack_data['blocks'][0]['text']['text']=domain+' is down'
                response = requests.post(webhook_url, data=json.dumps(slack_data)
                ,headers={'Content-Type': 'application/json'})

    else:
        print("invalid domain")


j=0
while True:
    if j < list_length:
        threads= []
        for i in range(j,j+50):
            if i < list_length:
                th=threading.Thread(target=status_code(domain_list[i].strip()))
                th.start()
                threads.append(th)
        for t in threads:
            t.join()
        j=j+50    
    else:
        break


