import urllib2, ssl, os
import xml.etree.ElementTree as ET
from datetime import datetime
from threading import Timer

meal = ['*☀ 조식 ☀*️', '*🕐 중식 🕐*', '*🌙 석식 🌙*']

bot_token = os.environ['TELEGRAM_BOT_TOKEN']

context = ssl._create_unverified_context()

def create_timer():
    today = datetime.today()
    tomorrow = today.replace(day=today.day+1, hour=6, minute=0, second=0, microsecond=0)
    time = tomorrow - today
    
    t = Timer(time.seconds+1, bot)
    t.start()

def bot():
    parser = ET.XMLParser(encoding="utf-8")
    
    page = ''
    
    for line in urllib2.urlopen('https://ksa.hs.kr/Home/CafeteriaMenu/72', context=context):
        if not '<link' in line and not '<meta' in line and not '<input' in line and not 'DOCTYPE' in line and not '<img' in line:
            if not '&amp' in line:
                page += line.replace('&', ' ')
            else:
                page += line
    
    root = ET.fromstring(page, parser=parser)
    
    menu = ''
    
    for i, item in enumerate(root.findall(".//table[@class='table table-bordered meal']//li")):
        menu += meal[i].decode('utf-8') + item.text+ '\n'
        
    menu = menu.strip().encode('utf-8')
    
    if menu is not '':
        url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=@ksameals&parse_mode=Markdown&text=' + urllib2.quote(menu)
        print urllib2.urlopen(url).readlines()
        
    create_timer()

create_timer()