import threading
import requests
import re
with open('domains-list.txt') as domains:
    domain_list = domains.readlines()

list_length= len(domain_list)

def status_code(domain):
    status_code=str(requests.head('http://'+domain+'', headers={'User-Agent': 'Foo bar'},allow_redirects=True).status_code)
    if re.match( r'[2,3]\d{2}$' ,status_code(d.strip())):
        print("status ok")
n=0
for i in range(n,n+50)
