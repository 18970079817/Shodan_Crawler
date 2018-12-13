import requests, sys
from bs4 import BeautifulSoup

def check_ip_range(iprange):
    def check_ip(ipaddr):
        try:
            addr = ipaddr.strip().split('.')
        except:
            print "Wrong IP format."
            sys.exit()
        if len(addr) != 4: 
            print "IP address is less than 4 parts."
            sys.exit()
        for i in range(4):
            try:
                addr[i]=int(addr[i])
            except:
                print "IP address has ilegal numbers."
                sys.exit()
            if addr[i]<=255 and addr[i]>=0:
                pass
            else:
                print "IP address out of range."
                sys.exit()
    try:
        start_ip = iprange.split('-')[0]
    except:
        print "First IP wrong IP format."
        sys.exit()
    try:
        end_ip = iprange.split('-')[1]
    except:
        print "Second IP wrong IP format."
        sys.exit()
    check_ip(start_ip)
    check_ip(end_ip)
    if int(end_ip.split('.')[3]) <= int(start_ip.split('.')[3]):
        if int(end_ip.split('.')[2]) <= int(start_ip.split('.')[2]):
            if int(end_ip.split('.')[1]) <= int(start_ip.split('.')[1]):
                if int(end_ip.split('.')[0]) <= int(start_ip.split('.')[0]):
                    print "Second IP is small than first IP."
                    sys.exit()

def get_ip(ipaddr):
    a = ipaddr.split('.')
    return a

iprange = raw_input('Please input the ip range,\nsuch as xxx.xxx.xxx.xxx-xxx.xxx.xxx.xxx:')
check_ip_range(iprange)
start_ip = iprange.split('-')[0]
end_ip = iprange.split('-')[1]

int_ip = lambda x: '.'.join([str(x/(256**i)%256) for i in range(3,-1,-1)])
ip_int = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])

for i in range(ip_int(start_ip), ip_int(end_ip)+1):
    try:
        r = requests.get('https://www.shodan.io/host/' + int_ip(i))
    except:
        print 'Some errors happened, check your network or something else.'
    else:
        soup = BeautifulSoup(r.text, 'lxml')
        for tbody in soup.find_all('tbody'):
            for tr in soup.find_all('tr'):
                print tr.find('td').string
                print tr.find('th').string
        for ul in soup.find_all('ul', class_ = 'ports'):
            for li in ul.find_all('li'):
                print li.find('a').string