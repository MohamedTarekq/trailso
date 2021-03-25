import requests
import json
import re
import argparse
from termcolor import colored 

print(colored("________   ______       ____      _____   _____        _____     ____    ", "red", attrs=['bold']))
print(colored("(___  ___) (   __ \     (    )    (_   _) (_   _)      / ____\   / __ \   ", "red", attrs=['bold']))
print(colored("    ) )     ) (__) )    / /\ \      | |     | |       ( (___    / /  \ \  ", "red", attrs=['bold']))
print(colored("   ( (     (    __/    ( (__) )     | |     | |        \___ \  ( ()  () ) ", "red", attrs=['bold']))
print(colored("    ) )     ) \ \  _    )    (      | |     | |   __       ) ) ( ()  () ) ", "red", attrs=['bold']))
print(colored("   ( (     ( ( \ \_))  /  /\  \    _| |__ __| |___) )  ___/ /   \ \__/ /  ", "red", attrs=['bold']))
print(colored("   /__\     )_) \__/  /__(  )__\  /_____( \________/  /____/     \____/  v1.0  ", "red", attrs=['bold']))
print(" ")
print(colored("                  Coded by ", "white", attrs=['bold']) + colored("Mohamed Tarek", "yellow", attrs=['bold']))
print(colored("         Twitter: ", "white", attrs=['bold']) + colored("https://twitter.com/timooon107", "yellow", attrs=['bold']))
print(colored("\n[+]An Automation Tool Based on","white", attrs=['bold'])+ colored(" [ securitytrails.com ]\n","green",attrs=['bold']))                                                                      

parser = argparse.ArgumentParser(description='An Automation Tool Based on securitytrails.com')
parser.add_argument("-c","--config",help="To store your APIKEY",action="store_true" )
parser.add_argument("-d","--domain",help="Domain name")
parser.add_argument("-s","--subs",help=" Get subdomains for a given domain",action="store_true")
parser.add_argument("-e","--extract",help="Extract all ips from (txt|a) historical dns records ",action="store_true")
parser.add_argument("-r","--record",help="Domain name",choices=['a','txt','A','TXT'])
parser.add_argument("-i","--ip",help="Ip of domain name" )
parser.add_argument("-l","--explore",help="Get the neighbors of a given IP address range",action="store_true")
parser.add_argument("-o","--output",help="Save the output in file")
args = parser.parse_args()

output = args.output
domain = args.domain
ip = args.ip
dns_record = args.record
page = "1"
if args.config:
    print("Enter your APIKEY:",end='')
    api = input()
    with open(".apikey.txt",'w')as txt:
        txt.write(api)
        txt.close
    raise SystemExit(colored("Your APIKEY is saved in .apikey.txt","cyan",attrs=['bold']))    
try :
    APIKEY = open('.apikey.txt','r').readline()
except :
    raise SystemExit(colored("Your APIKEY doesn't exist\nplease add one by write\n","red",attrs=['bold'])+colored("python3 trailso.py --config","cyan",attrs=['bold']))
  
headers = {
        "Accept": "application/json",
        "APIKEY": APIKEY
    }

def save(i,output):
    with open(output,'a') as txt:
        txt.write(str(i))
        
def explorer(ip):
    url = f"https://api.securitytrails.com/v1/explore/ip/{ip}"
    req = requests.request("GET", url, headers=headers)
    return req.content

def dns_history(domain,dns_record,page="1"):
    dns_record_lower = dns_record.lower()
    url = f"https://api.securitytrails.com/v1/history/{domain}/dns/{dns_record_lower}"
    req = requests.request("GET", url, headers=headers, params={"page":page})
    return req.text

def Subdomains(domain):
    subdomains = []
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    req = requests.request("GET", url, headers=headers)
    cont = req.content
    dic = json.loads(cont)
    for sub in dic["subdomains"]:
        subdomains.append(sub+"."+domain)
    return subdomains    

if domain and args.subs:
    subs = Subdomains(domain) 
    for i in subs:
        print(colored(f"{i}","green",attrs=['bold']))
        if output:
            i = i+"\n"
            save(i,output)
elif ip and args.explore:
    explor = explorer(ip)
    res = json.loads(explor)
    for i in res["blocks"]:
      split = str(i["ip"]).split("/")[0]
      print(split+" : ",end='')
      if output:
          j = split+" : "
          save(j,output)
          if not i["hostnames"]:
              save("\n",output)
      for host in i["hostnames"]:
        print(colored(f"{host}","green",attrs=['bold'])+",",end='')
        if output:
            j = host+","
            save(j,output)
      print()
    cidr =  str(i["ip"]).split("/")[1] 
    print(colored(f"CIDR for this ip --> {ip}/{cidr}","green",attrs=['bold']))  
elif domain and args.extract and dns_record:
    dns_his = dns_history(domain,dns_record,page)
    ip = re.findall(r'\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b',dns_his)
    for i in ip : 
      print(colored(f"{i}","green",attrs=['bold'])) 
      if output:
          j = i+"\n"
          save(j,output)    
else:
    raise SystemExit(colored("Please check arguments","red",attrs=['bold'])+"\n"+colored("if you want subdomains  you must add","cyan",attrs=['bold'])+" --subs -d example.com\n"+colored("if you want extract all ips you must add","cyan",attrs=['bold'])+" --extract -d example.com --record (txt|a)\n"+colored("if you want explore the ip you must add","cyan",attrs=['bold'])+" --ip 10.10.10.10 --explore\n"+colored("Happy Hacking","green",attrs=['bold']))