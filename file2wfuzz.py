#/usr/bin/python3

import argparse
from copy import copy, deepcopy

import time

class pkt:
    def __init__(self, method: str,url: str,headers: dict[str , str],body):
        self.url=url
        self.method=method
        self.headers=headers
        self.body=body

    def __str__(self):
        result = self.method + " : " + self.url
        for k, v in self.headers.items():
            result = result + k+": "+v+"\n"
        result= result +"\n"+ self.body
        return result
    
    def __copy__(self):
        return type(self)(self.method, self.url,self.headers,self.body)

    def __deepcopy__(self, memo): 
        id_self = id(self)    
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)(
                deepcopy(self.method, memo), 
                deepcopy(self.url, memo),
                deepcopy(self.headers, memo),
                deepcopy(self.body, memo))
            memo[id_self] = _copy 
        return _copy

def load_packet(path):
    method=""
    headers={}
    body = ""
    with open(path,'r') as f:
        i=0
        isheader = True
        for line in f.readlines():
            line = line.replace('"','\\"')
            if i==0:
                words = line.split(" ")
                method=words[0]
            elif line == "\n":
                isheader = False
            elif isheader:
                element = line.split(":")
                headers[element[0]]= ":".join(element[1:]).replace("\n","")[1:] 
            else:
                line = line.replace("\n","")
                if body == "":
                    body = line
                else:
                    body = body + "\n" + line            
            i=i+1
    return pkt(method,url,headers,body)


def get_headers(pkt):
        result = ""
        for k, v in pkt.headers.items():
            result = result + '-H "'+k+": "+v+'" '
        return result



parser = argparse.ArgumentParser(description='file2wfuzz is a simple python script to generate a wfuzz command line from a package provided in a file. \n usage: "file2wfuzz -w /usr/share/wfuzz/wordlist/Injections/bad_chars.txt -u http://target/FUZZ -p "./pkt.txt"')
parser.add_argument("--wordlist", "-w", help="wordlist path", default="<wordlist>")
parser.add_argument("--url", "-u", help="", default="<url>")
parser.add_argument("--pkt", "-p", help="packet path", required=True)
args = parser.parse_args()



path = args.pkt
url="http://localhost:9090/"
mypkt = load_packet(path) 
if mypkt.body == "":
    print("wfuzz -z file,"+args.wordlist+" "+ get_headers(mypkt)+" "+args.url)
else:
    print("wfuzz -z file,"+args.wordlist+" "+ get_headers(mypkt)+ " -d \""+mypkt.body+"\" "+args.url)

