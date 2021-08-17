import time
import requests
import sys
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

gitam_id = '<glearn_id>'
gitam_pass = '<gitam_google_password>'
glearn_pass = '<glearn_password>'
zoom_name = '<zoom_account_name>'

def value(soup, element):
    try:
        return soup.find(id=element)['value']
    except:
        return ''
        
def send(text):
    token = '<telegeram_bot_token>'
    chat_id = '<telegram_user_chat_id>'
    requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=HTML')

def month(n):
    n = n.lower()
    if n == 'jan':
        return '01'
    elif n == 'feb':
        return '02'
    elif n == 'mar':
        return '03'
    elif n == 'apr':
        return '04'
    elif n == 'may':
        return '05'
    elif n == 'jun':
        return '06'
    elif n == 'jul':
        return '07'
    elif n == 'aug':
        return '08'
    elif n == 'sep':
        return '09'
    elif n == 'oct':
        return '10'
    elif n == 'nov':
        return '11'
    else:
        return '12'

def n2s(s,n):
    if n < 10:
        return ('0'*(s-1))+str(n)
    else:
        return str(n)
    
def stamp(n):
    now = datetime.now()
    return datetime(now.year, now.month, now.day, n[0], n[1]).timestamp()

def convert(n):
    if n.find('AM') < 0:
        t = n.split('PM')[0].split(':')
        if t[0] == '12':
            return [int(t[0]),int(t[1])]
        else:
            return [int(t[0])+12, int(t[1])]
    else:
        t = n.split('AM')[0].split(':')
        if t[0] == '12':
            return [0,int(t[1])]
        else:
            return [int(t[0]),int(t[1])]

def getonlineclasses():
    r = requests.get('https://login.gitam.edu/Login.aspx')
    soup = BeautifulSoup(r.content, 'lxml')
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    data = {
          '__EVENTTARGET': value(soup,'__EVENTTARGET'),
          '__EVENTARGUMENT': value(soup,'__EVENTARGUMENT'),
          '__VIEWSTATE': value(soup,'__VIEWSTATE'),
          '__VIEWSTATEGENERATOR': value(soup,'__VIEWSTATEGENERATOR'),
          '__EVENTVALIDATION': value(soup,'__EVENTVALIDATION'),
          'txtusername': str(gitam_id),
          'password': glearn_pass,
          'Submit': 'Login'
        }
    with requests.Session() as s:
        r = s.post('https://login.gitam.edu/Login.aspx', data = data, headers = headers)
        r = s.get('https://login.gitam.edu/route.aspx?id=GLEARN&type=S')
        glearn = BeautifulSoup(r.content, 'lxml')
                
    classlist = []
    for i in glearn.find(id='ContentPlaceHolder1_GridViewonline').find_all('a'):
        now = datetime.now()
        date_time = i.find('h6').text.split('Date : ')[1].split('  :: Time:')
        date_raw = date_time[0].split('-')
        date = f'{date_raw[0]}/{month(date_raw[1])}/{date_raw[2]}'
        if date == now.strftime('%d/%m/%Y'):
            times = date_time[1].strip().split(' to ')
            classlist.append({
                'name': i.find('h4').text.split(' on ')[1].split(' created ')[0].strip(),
                'link': i['href'].strip().replace('/j/', '/wc/join/'),
                'start': stamp(convert(times[0])),
                'end': stamp(convert(times[1])),
            })
    for i in range(len(classlist)-1):
        for j in range(0,len(classlist)-i-1):
            if classlist[j]['start'] > classlist[j+1]['start']:
                classlist[j], classlist[j+1] = classlist[j+1], classlist[j]
    poplist = []
    for i in range(len(classlist)-1):
        if classlist[i]['name'] == classlist[i+1]['name']:
            classlist[i+1]['start'] = classlist[i]['start']
            poplist.append(i)
    for i in poplist:
        classlist.pop(i)
    return classlist
    
def intime(end):
    if datetime.now().timestamp() < (end-30):
        return True
    else:
        return False

def inday():
    now = datetime.now()
    if now.weekday() in range(5):
        return True
    else:
        return False
    
def inhour():
    if int(datetime.now().strftime('%H')) in range(9,17):
        return True
    else:
        return False
    
def beforetime():
    if int(datetime.now().strftime('%H')) in range(0,9):
        return True
    else:
        return False
    
def aftertime():
    if int(datetime.now().strftime('%H')) in range(16,24):
        return True
    else:
        return False
    
def browser():
    global driver
    options = Options()
    options.headless = True
    options.set_preference("media.volume_scale", "0.0")
    options.set_preference('permissions.default.microphone', 1)
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
    driver = webdriver.Firefox(options=options)
    driver.get('https://zoom.us/google_oauth_signin')
    email_field_inactive = True
    next_button_inactive = True
    password_field_inactive = True
    not_logged_in = True
    while email_field_inactive:
        try:
            driver.find_element_by_xpath("//input[@aria-label='Email or phone']").send_keys(gitam_id+'@gitam.in')
            time.sleep(2)
            email_field_inactive = False
        except:
            pass
    while next_button_inactive:
        try:
            driver.find_element_by_class_name('VfPpkd-RLmnJb').click()
            next_button_inactive = False
        except:
            pass
    while password_field_inactive:
        try:
            driver.find_element_by_xpath("//input[@aria-label='Enter your password']").send_keys(gitam_pass)
            time.sleep(2)
            password_field_inactive = False
        except:
            pass
    next_button_inactive = True
    while next_button_inactive:
        try:
            driver.find_element_by_class_name('VfPpkd-RLmnJb').click()
            next_button_inactive = False
        except:
            pass
    while not_logged_in:
        try:
            if zoom_name in driver.page_source:
                not_logged_in = False
        except:
            pass
    driver.get('https://zoom.us')

def zoom(course):
    browser()
    driver.get(course['link'])
    joinBtn_inactive = True
    while joinBtn_inactive:
        try:
            driver.find_element_by_id('joinBtn').click()
            joinBtn_inactive = False
        except:
            pass
    print('')
    sys.stdout.write('\r'+'Waiting...')
    audio_not_joined = True
    time.sleep(20)
    i = 0
    while audio_not_joined:
        if intime(course['end']):
            try:
                if driver.find_element_by_class_name('join-audio-container__btn').text == 'Join Audio':
                    time.sleep(5)
                    i+=1
                    try:
                        driver.find_element_by_class_name('join-audio-by-voip__join-btn').click()
                        i+=1
                    except:
                        driver.find_element_by_class_name('join-audio-container__btn').click()
                        i+=1
                else:
                    audio_not_joined = False
            except:
                time.sleep(10)
                pass
        else:
            audio_not_joined = False
    print('\r'+f'Attending {course["name"]}')
    send(f'Attending {course["name"]}')
    size = len(str(int((course["end"] - datetime.now().timestamp())/60)))
    while datetime.now().timestamp() < (course['end']):
        sys.stdout.write('\r'+f'Class ends in {n2s(size, int((course["end"] - datetime.now().timestamp())/60))} minutes. ')
        time.sleep(30)
    driver.close()
    
while True:
    if inday():
        if inhour():
            try:
                oclist = getonlineclasses()
                attend = ''
                now = int(datetime.now().timestamp())
                for oc in oclist:
                    if (now >= oc['start']) and (now < oc['end']-1200):
                        attend = oc
                        break
                if attend != '':
                    zoom(attend)
                else:
                    for i in range(60):
                        sys.stdout.write('\r'+f'Checking in {n2s(2,60-i)}')
                        time.sleep(1)
            except Exception as e:
                print('Error:', e)
                time.sleep(60)
        if beforetime():
            print('\nSleeping till 09:00AM')
            sleeptime = datetime.now().replace(hour = 9, minute = 0, second = 0).timestamp() - datetime.now().timestamp()
            size = len(str(int(sleeptime/60)))
            while sleeptime > 0:
                sys.stdout.write('\r'+f'Minutes: {n2s(size, int(sleeptime/60))}')
                time.sleep(30)
                sleeptime = datetime.now().replace(hour = 9, minute = 0, second = 0).timestamp() - datetime.now().timestamp()
        if aftertime():
            print('\nDone for today.')
            time.sleep((datetime.now()+timedelta(days=1)).replace(hour = 0, minute = 0, second = 0).timestamp() - datetime.now().timestamp() + 1)
    else:
        print('\nNothing today.')
        time.sleep((datetime.now()+timedelta(days=1)).replace(hour = 0, minute = 0, second = 0).timestamp() - datetime.now().timestamp() + 1)
