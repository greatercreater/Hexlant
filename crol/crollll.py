import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime, date, timedelta
import sqlite3
import telegram


def CompareandSet(title, date, link, exchange):
    con=sqlite3.connect("crol/crol_db.sqlite")
    cur=con.cursor()

    cur.execute("select * from notice_"+exchange)
    Indb=list(cur.fetchall())
    con.close()

    arr=dict()

    for n in range(len(link)):
        
        if len(Indb) <= n:
            print("이상이상"+exchange)
            print("Indb: ",len(Indb))
            print("n: ",n)
            break
        else:
            pass

        for i in Indb:
            if (link[n]==i[2]) and (title[n]==i[0]):
                break
            elif link[n]==i[2] and not title[n]==i[0]:
                arr[n]="mod"
                break
            else:
                continue
        else:
            arr[n]="new"
    
    return arr


def send2U(arr,title,date,link,exchange):
    my_token='1339037346:AAHOFfZQZb5qqRV_xacyyVyhQb9-qaXWIFE'

    bot=telegram.Bot(token=my_token)
    #updates= bot.getUpdates()
    #chat_ID=updates[-1].message.chat.id
    #mychannel_num
    chat_ID=1034101411
    
    cur_time=datetime.now().strftime("%c")
    con=sqlite3.connect("crol/crol_db.sqlite")
    cur=con.cursor()
    for a in arr:
        if arr[a]=="new":
            bot.sendMessage(chat_id=chat_ID, text='<<New notice from '+exchange+'>>')
            bot.sendMessage(chat_id=chat_ID, text=title[a]+"\nUpload Date: "+date[a]+"\n"+link[a])
            cur.execute("insert into notice_"+exchange+" values(?,?,?,?,?,?)",(title[a],date[a],link[a],exchange,cur_time,''))
        elif arr[a]=="mod":
            bot.sendMessage(chat_id=chat_ID, text='<Correction occured on '+exchange+'>')
            bot.sendMessage(chat_id=chat_ID, text=title[a]+"\nUpload Date: "+date[a]+"\n"+link[a])
            cur.execute("update notice_"+exchange+" set TITLE = ?, DB_MODIFIED = ? where LINK = ?",(title[a],cur_time,link[a]))
        else:
            print("이상이상2")
    
    con.commit()
    con.close()


def GetandCompareandSet():
    now=datetime.now()
    driver= webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')


    #get notices of Upbit
    uurl='https://upbit.com/service_center/notice'
    driver.get(uurl)

    time.sleep(6)
    source=driver.page_source
    u_ttemp=driver.find_element_by_tag_name('tbody tr').find_elements_by_xpath('//td[1]')
    u_dtemp=driver.find_element_by_tag_name('tbody tr').find_elements_by_xpath('//td[2]')

    soup=BeautifulSoup(source, 'html.parser')
    u_temp=soup.select('tbody tr td a')
    u_emBlue=soup.select('tbody tr.emBlue td.lAlign')
    u_top=soup.select('tbody tr.top td.lAlign')

    u_length=0
    link=[]
    title=[]
    dates=[]
    for j in u_temp:
        link.append(j.get('href'))
    for j in u_ttemp:
        title.append(j.text)
    for j in u_dtemp:
        dates.append(j.text)
        u_length+=1

    n=0
    for j in u_emBlue:
        title.remove(j.text)
        link.pop(0)
        n+=1
    
    n=0
    for j in u_top:
        title.pop(0)
        dates.pop(0)
        link.pop(0)
        n+=1
    u_length-=n

    base_board='https://upbit.com'
    i=0
    while i<u_length:
        link[i]=base_board+link[i]
        i+=1

    arr=CompareandSet(title, dates, link, "upbit")
    send2U(arr,title,dates,link,"upbit")


    #get notices of Bithumb
    burl='https://cafe.bithumb.com/view/boards/43'
    driver.get(burl)

    time.sleep(2)
    source=driver.page_source
    soup=BeautifulSoup(source, 'html.parser')
    title=soup.select("tbody tr[style*='white'] td.one-line")
    dates=soup.select("tbody tr[style*='white'] td.small-size")[1::2]

    b_length=0
    for j in dates:
        b_length+=1
    for i in range(b_length):
        dates[i]=dates[i].text
        title[i]=title[i].text

    i=0
    for j in dates:
        if(j.find(":")==-1):
            i+=1
            continue
        else:
            if int(j[1:3])>now.hour:
                yesterday=date.today()-timedelta(1)
                dates[i]=yesterday.strftime('%Y.%m.%d')
            elif int(j[1:3])<now.hour:
                dates[i]=date.today().strftime('%Y.%m.%d')
            else:
                if int(j[4:6])>now.minute:
                    yesterday=date.today()-timedelta(1)
                    dates[i]=yesterday.strftime('%Y.%m.%d')
                else:
                    dates[i]=date.today().strftime('%Y.%m.%d')
            i+=1

    b_temp=soup.select("tbody tr[style*='white']")
    link=[]
    string=''

    for j in b_temp:
        string=(j.get('onclick'))[15:22]
        link.append(string)

    base_board='https://cafe.bithumb.com/view/board-contents/'

    i=0
    while i<b_length:
        link[i]=base_board+link[i]
        i+=1

    arr=CompareandSet(title, dates, link, "bithumb")
    send2U(arr,title,dates,link,"bithumb")


    #get notices of Coinone
    curl='https://coinone.co.kr'
    driver.get(curl)

    time.sleep(6)
    source=driver.page_source
    soup=BeautifulSoup(source, 'html.parser')

    title=soup.select('div.pc-notice-dropdown .notice-title')
    dates=soup.select('div.pc-notice-dropdown .notice-date')

    c_temp=soup.select('div.pc-notice-dropdown a.notice-link')
    link=[]
    c_length=0
    for j in c_temp:
        link.append(j.get('href'))
        c_length+=1

    i=0
    while i<c_length:
        link[i]=curl+link[i]
        title[i]=title[i].text
        dates[i]=dates[i].text
        i+=1
    driver.quit()

    arr=CompareandSet(title, dates, link, "coinone")
    send2U(arr,title,dates,link,"coinone")


    #get notices of Korbit
    kurl='https://korbitblog.tumblr.com/'

    source=requests.get(kurl)
    soup=BeautifulSoup(source.text, 'html.parser')

    title=soup.select('h1 a')
    k_dtemp=soup.select('a time')
    dates=[]
    k_length=0
    for j in k_dtemp:
        dates.append(j.get('datetime'))
        k_length+=1

    i=0
    while i<k_length:
        dates[i]=(dates[i])[:10]
        dates[i]=(dates[i]).replace("-",".")
        i+=1

    k_temp=title
    link=[]
    for j in k_temp:
        link.append(j.get('href'))

    for i in range(k_length):
        title[i]=title[i].text
    
    arr=CompareandSet(title, dates, link, "korbit")
    send2U(arr,title,dates,link,"korbit")
    



'''
print('------------------')
print('  THIS IS UPBIT')
print('------------------')
for c in u_title:
    print(c)
for c in u_date:
    print(c)
for c in u_link:
    print(c)
print('------------------')
print('  THIS IS BITHUMB')
print('------------------')
for c in b_title:
    print(c)
for c in b_date:
    print(c)
for c in b_link:
    print(c)
print('------------------')
print('  THIS IS COINONE')
print('------------------')
for c in title:
    print(c)
for c in dates:
    print(c)
for c in link:
    print(c)
print('------------------')
print('  THIS IS KORBIT')
print('------------------')
for c in title:
    print(c)
for c in dates:
    print(c)
for c in link:
    print(c)
'''


