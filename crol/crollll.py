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


def send2U(arr,bot,chat_ID,title,date,link,exchange):
    cur_time=datetime.now().strftime("%c")
    con=sqlite3.connect("crol/crol_db.sqlite")
    cur=con.cursor()
    for a in arr:
        if arr[a]=="new":
            bot.sendMessage(chat_id=chat_ID, text='<<New notice from '+exchange+'>>')
            bot.sendMessage(chat_id=chat_ID, text=title[a]+"\nUpload Date: "+date[a]+"\n"+link[a])
            #cur.execute("insert into notice_"+exchange+" values(?,?,?,?,?,?)",(title[a],date[a],link[a],exchange,cur_time,''))
        elif arr[a]=="mod":
            bot.sendMessage(chat_id=chat_ID, text='<Correction occured on '+exchange+'>')
            bot.sendMessage(chat_id=chat_ID, text=title[a]+"\nUpload Date: "+date[a]+"\n"+link[a])
            #cur.execute("update notice_"+exchange+" set TITLE = ?, DB_MODIFIED = ? where LINK = ?",(title[a],cur_time,link[a]))
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

    u_length=0
    u_link=[]
    u_title=[]
    u_date=[]
    for j in u_temp:
        u_link.append(j.get('href'))
    for j in u_ttemp:
        u_title.append(j.text)
    for j in u_dtemp:
        u_date.append(j.text)
        u_length+=1

    n=0
    for j in u_emBlue:
        u_title.remove(j.text)
        n+=1
    for i in range(n):
        u_link.pop(0)

    base_board='https://upbit.com'
    i=0
    while i<u_length:
        u_link[i]=base_board+u_link[i]
        i+=1


    #get notices of Bithumb
    burl='https://cafe.bithumb.com/view/boards/43'
    driver.get(burl)

    time.sleep(2)
    source=driver.page_source

    soup=BeautifulSoup(source, 'html.parser')
    b_title=soup.select('tbody tr td.one-line')
    b_date=soup.select('tbody tr td.small-size')[1::2]

    b_length=0
    for j in b_date:
        b_length+=1
    for i in range(b_length):
        b_date[i]=b_date[i].text
        b_title[i]=b_title[i].text

    i=0
    for j in b_date:
        if(j.find(":")==-1):
            i+=1
            continue
        else:
            if int(j[1:3])>now.hour:
                yesterday=date.today()-timedelta(1)
                b_date[i]=yesterday.strftime('%Y.%m.%d')
            elif int(j[1:3])<now.hour:
                b_date[i]=str(now.year)+"."+str(now.month)+"."+str(now.day)
            else:
                if int(j[4:6])>now.minute:
                    yesterday=date.today()-timedelta(1)
                    b_date[i]=yesterday.strftime('%Y.%m.%d')
                else:
                    b_date[i]=str(now.year)+'.'+str(now.month)+'.'+str(now.day)
            i+=1

    b_temp=soup.select('tbody tr')
    b_link=[]
    string=''

    for j in b_temp:
        string=(j.get('onclick'))[15:22]
        b_link.append(string)

    base_board='https://cafe.bithumb.com/view/board-contents/'

    i=0
    while i<b_length:
        b_link[i]=base_board+b_link[i]
        i+=1


    #get notices of Coinone
    curl='https://coinone.co.kr'
    driver.get(curl)

    time.sleep(6)
    source=driver.page_source
    soup=BeautifulSoup(source, 'html.parser')

    c_title=soup.select('div.pc-notice-dropdown .notice-title')
    c_date=soup.select('div.pc-notice-dropdown .notice-date')

    c_temp=soup.select('div.pc-notice-dropdown a.notice-link')
    c_link=[]
    c_length=0
    for j in c_temp:
        c_link.append(j.get('href'))
        c_length+=1

    i=0
    while i<c_length:
        c_link[i]=curl+c_link[i]
        c_title[i]=c_title[i].text
        c_date[i]=c_date[i].text
        i+=1
    driver.quit()


    #get notices of Korbit
    kurl='https://korbitblog.tumblr.com/'

    source=requests.get(kurl)
    soup=BeautifulSoup(source.text, 'html.parser')

    k_title=soup.select('h1 a')
    k_dtemp=soup.select('a time')
    k_date=[]
    k_length=0
    for j in k_dtemp:
        k_date.append(j.get('datetime'))
        k_length+=1

    i=0
    while i<k_length:
        k_date[i]=(k_date[i])[:10]
        k_date[i]=(k_date[i]).replace("-",".")
        i+=1

    k_temp=k_title
    k_link=[]
    for j in k_temp:
        k_link.append(j.get('href'))

    for i in range(k_length):
        k_title[i]=k_title[i].text
    
    my_token='1339037346:AAHOFfZQZb5qqRV_xacyyVyhQb9-qaXWIFE'

    bot=telegram.Bot(token=my_token)
    updates= bot.getUpdates()
    chat_ID=updates[-1].message.chat.id

    u_arr=CompareandSet(u_title, u_date, u_link, "upbit")
    b_arr=CompareandSet(b_title, b_date, b_link, "bithumb")
    c_arr=CompareandSet(c_title, c_date, c_link, "coinone")
    k_arr=CompareandSet(k_title, k_date, k_link, "korbit")

    send2U(u_arr,bot,chat_ID,u_title,u_date,u_link,"upbit")
    send2U(b_arr,bot,chat_ID,b_title,b_date,b_link,"bithumb")
    send2U(c_arr,bot,chat_ID,c_title,c_date,c_link,"coinone")
    send2U(k_arr,bot,chat_ID,k_title,k_date,k_link,"korbit")







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
for c in c_title:
    print(c)
for c in c_date:
    print(c)
for c in c_link:
    print(c)
print('------------------')
print('  THIS IS KORBIT')
print('------------------')
for c in k_title:
    print(c)
for c in k_date:
    print(c)
for c in k_link:
    print(c)
'''


