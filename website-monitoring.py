import threading
import requests
import re
with open('domains-list.txt') as domains:
    domain_list = domains.readlines()

list_length= len(domain_list)

def status_code(domain):
    status_cod=str(requests.head('http://'+domain+'', headers={'User-Agent': 'Foo bar'},allow_redirects=True).status_code)
    if re.match( r'[2,3]\d{2}$' ,status_cod.strip()):
        print("status ok")
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


