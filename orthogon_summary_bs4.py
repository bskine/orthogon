'''
orthogon_scrape.py...........Using beautifulsoup4 to scrape the status page of various radio's and provide info on hostname, sitelocation,
power, rssi, modulation, and capacity.  Includes current temp, date, and time at beginning of output.  Prints output to shell as well as to text file
in same directory.
'''

#! usr/bin/env python
from bs4 import BeautifulSoup
import urllib, urllib.request
from datetime import datetime
import time
import requests
from requests import ConnectionError


dt = datetime.now().time()
dt = dt.replace(microsecond=0)
dt_date = datetime.now().date()
current_date = (dt_date.strftime('%m/%d/%Y')) # formatting date to mm/dd/yyy

orth = [ '71', '73', '75', '77', '79', '80', '87', '88', '95', '96', '81', '82']

theurl = 'https://w1.weather.gov/obhistory/PAQT.html'
thepage = urllib.request.urlopen(theurl)
soup = BeautifulSoup(thepage, features="lxml")
current_temp = soup.find_all('td')[14].text
current_temp = int(current_temp)
canadian_temp =(current_temp -32)*(5/9)
local_weather =(str(current_temp) + 'F/' + str(int(canadian_temp)) + 'C')

with open('orthogon_scrolling.txt', 'a+') as f: 
    print('{:^50}{:^50}{:^50}'.format(('.'*10), ('.'*10), ('.'*10)))
    f.write('{:^50}{:^50}{:^50}'.format(('.'*10), ('.'*10), ('.'*10)) + '\n')
    print('{:^50}{:^50}{:^50}'.format(local_weather, current_date, str(dt)))
    f.write('{:^50}{:^50}{:^50}'.format(local_weather, current_date, str(dt)) + '\n')
    print('{:^50}{:^50}{:^50}'.format(('.'*10), ('.'*10), ('.'*10)))
    f.write('{:^50}{:^50}{:^50}'.format(('.'*10), ('.'*10), ('.'*10)) + '\n')
    print('*'*175)
    f.write('*'*175 + '\n')
    print('{:<15}{:^15}{:^15}{:^15}{:^15}{:^45}{:>35}{:>20}'.format('Linkname', 'IP', 'Site', 'TX Power/Max', 'RSSI', 'TX MOD/RX MOD', 'Modulation Detail', 'Link Capacity'))
    f.write('{:<15}{:^15}{:^15}{:^15}{:^15}{:^45}{:>35}{:>20}'.format('Linkname', 'IP', 'Site','TX Power/Max', 'RSSI', 'TX MOD/RX MOD', 'Modulation Detail', 'Link Capacity') + '\n')
    print('*'*175 + '\n')
    f.write(('*'*175+ '\n'))
    for s in orth:
        try:
            s = ('10.27.11.'+str(s))
            url_address = 'http://' + str(s) + '/top.cgi?xsrf=&1'
            status_page = urllib.request.urlopen(url_address)
            status = BeautifulSoup(status_page, features='lxml')
            hostname = status.find('div', id= 'pageBody').find('div', id='linkName').get('title')
            
            site_name = status.find('div', id= 'pageBody').find('div', id= 'siteName').text.strip('\n')
            tx_power = status.find('div', id= 'pageBody').find_all('tr')[7].find_all('td')[3].text
            max_tx_power = status.find('div', id= 'pageBody').find_all('tr')[5].find_all('td')[5].text.strip('\n')
            hardware = status.find('div', id= 'pageBody').find('div', id='hardwareVersion').get('title')
            if hardware.startswith('B'):
                try:
                    rx_power = status.find('div', id= 'pageBody').find_all('div')[26].text.strip(',')
                    tx_mod = status.find('div', id= 'pageBody').find_all('tr')[22].find_all('td')[5].text
                    rx_mod = status.find('div', id= 'pageBody').find_all('tr')[23].find_all('td')[5].text
                    link_capacity = status.find('div', id= 'pageBody').find_all('tr')[21].find_all('td')[5].text.strip('\n')
                    mod_detail = status.find('div', id= 'pageBody').find_all('tr')[25].find_all('td')[5].text.strip('\n')
                except:
                    mod_detail = status.find('div', id= 'pageBody').find_all('tr')[25].find_all('td')[3].text.strip('\n')
            elif hardware.startswith('D'):
                rx_power = status.find('div', id= 'pageBody').find_all('div')[25].text.strip(',')
                tx_mod = status.find('div', id= 'pageBody').find_all('tr')[19].find_all('td')[5].text
                rx_mod = status.find('div', id= 'pageBody').find_all('tr')[20].find_all('td')[5].text
                link_capacity = status.find('div', id= 'pageBody').find_all('tr')[18].find_all('td')[5].text.strip('\n')
                mod_detail = status.find('div', id= 'pageBody').find_all('tr')[22].find_all('td')[5].text.strip('\n')
                time.sleep(.25)
            tx_mod = tx_mod.split() #removing duplicates
            tx_mod = tx_mod[0:2]
            tx_mod = ' '.join(tx_mod)
            print('{:<15}{:^15}{:^15}{:^15}{:^15}{:^45}{:>35}{:>20}'.format(hostname, s, site_name, (tx_power+'/'+max_tx_power),
                                                                rx_power, (tx_mod+'/'+rx_mod), mod_detail, (link_capacity+'Mbps')))
            f.write('{:<15}{:^15}{:^15}{:^15}{:^15}{:^45}{:>35}{:>20}'.format(hostname, s, site_name, (tx_power+'/'+max_tx_power),
                                                                rx_power, (tx_mod+'/'+rx_mod), mod_detail, (link_capacity+'Mbps')) + '\n')
            print('-'*175)
            f.write('-'*175 + '\n')
            time.sleep(1)
            f.write('\n')
        except(ConnectionError, TimeoutError, Exception) as e:
            print(s + ' has experienced a ' + str(e))
            f.write(str(e) + '\n')
            continue
        except HTTPError as e:
            print(e)
            f.write(e + '\n')
            continue
        except URLError:
            print(s + 'is offline')
            f.write(s + 'is offline' + '\n')
            continue
