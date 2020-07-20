import re
import time
import sqlite3
import telegram
from datetime import datetime, date, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup

class Notice:

    def __init__(self, idx, case, sourcelist, base_url, title_tag, day_tag, link_tag, day_att, link_att):
        self.title=''; self.day=''; self.link=''
        
        def time2date(former):
            raw_day=former.lstrip()
            p=re.compile(r'[0-9]{4}\D[0-9]{2}\D[0-9]{2}')
            sear=p.search(raw_day)
            if sear:                          #not case==0:
                if raw_day.find('-') == -1:
                    return raw_day
                else:
                    return sear.group().replace("-",".")
            else:
                if raw_day.find(":")==-1:
                    return raw_day
                else:
                    now=datetime.now()
                    h=int(raw_day[:2]); m=int(raw_day[3:5])
                    if h > now.hour or (h == now.hour and m > now.minute):
                        yesterday=date.today()-timedelta(1)
                        return yesterday.strftime('%Y.%m.%d')
                    else:
                        return date.today().strftime('%Y.%m.%d')
        
        def parse():
            try:
                self.title=sourcelist[idx].select_one(title_tag).get_text()
            except AttributeError as e:
                pass
            try:
                temp=sourcelist[idx].select_one(day_tag)
                if case==2:
                    self.day=time2date(temp.get(day_att))
                else:
                    self.day=time2date(temp.get_text())
            except AttributeError as e:
                pass
            try:
                if case==0:
                    self.link=base_url+sourcelist[idx].get(link_att)[15:22]
                else:
                    self.link=base_url+sourcelist[idx].select_one(link_tag).get(link_att)
            except AttributeError as e:
                pass
            
        parse()
        #AttributeError

class Exchanger:
    def __init__(self, case, url, base_url, title_tag, day_tag, link_tag, day_att, link_att):
        self.noticeset=[]
        self.case=case
        self.url=url; self.base_url=base_url
        self.title_tag = title_tag; self.day_tag = day_tag; self.link_tag = link_tag
        self.day_att=day_att; self.link_att=link_att
        
    def getData(self,driver,selector):
        driver.get(self.url)
        time.sleep(7)
        source=driver.page_source
        soup=BeautifulSoup(source,'html.parser')

        sourcelist=soup.select(selector)
        length=len(sourcelist)
        
        i=0
        while i<length:
            notice=Notice(i, self.case, sourcelist, self.base_url, self.title_tag, self.day_tag, self.link_tag, self.day_att, self.link_att)
            self.noticeset.append(notice)
            i+=1
        
    def CompareSend(self):
        cur_time=datetime.now().strftime("%c")
        exchanges={0:'bithumb',1:'coinone',2:'korbit',3:'upbit',}
        con=sqlite3.connect("crol/noticedb2.sqlite")
        cur= con.cursor()
        cur.execute("select * from notices where EXCHANGE = ?",(exchanges[self.case],))
        Indb=list(cur.fetchall())
        
        new=[]
        n=len(self.noticeset)-1; m=n

        while m >= 0:
            l = 0
            while l < m:
                if self.noticeset[m].link == self.noticeset[l].link:
                    self.noticeset.pop(l)
                    n-=1
                    break
                l+=1
            m-=1


        while n>=0:
            for i in Indb:
                if self.noticeset[n].title==i[0] and self.noticeset[n].link==i[2]:
                    break
                else:
                    continue
            else:
                new.append(n)
            n-=1
        
        my_token='1339037346:AAHOFfZQZb5qqRV_xacyyVyhQb9-qaXWIFE'
        bot=telegram.Bot(token=my_token)
        #id=1034101411
        id=-1001472766381  #channel id
        for i in new:
            bot.sendMessage(chat_id=id, text="<b>"+exchanges[self.case]+"</b>\n"+self.noticeset[i].title+"\n\nUpload Date: "+self.noticeset[i].day+"\n\n"+self.noticeset[i].link, parse_mode='HTML')
            cur.execute("insert into notices values(?,?,?,?,?)",(self.noticeset[i].title,self.noticeset[i].day,self.noticeset[i].link,exchanges[self.case],cur_time))
        con.commit()
        con.close()


def run():
    driver= webdriver.Chrome('C:/chromedriver_win32/chromedriver')
    time.sleep(1)
    B=Exchanger(0,'https://cafe.bithumb.com/view/boards/43','https://cafe.bithumb.com/view/board-contents/',"td.one-line","td:nth-child(3)",'','','onclick')
    B.getData(driver,"tbody > tr")
    C=Exchanger(1,'https://coinone.co.kr','https://coinone.co.kr','a > div > p.info-title > span','a > span','a','','href')
    C.getData(driver,'div.crypto-info > landing-main-notice-info > ul > li')
    K=Exchanger(2,'https://korbitblog.tumblr.com/','','h1 > a','a.post-date time','h1 > a','datetime','href')
    K.getData(driver,"div.posts.cf > article.post.post-text")
    U=Exchanger(3,'https://upbit.com/service_center/notice','https://upbit.com','td.lAlign > a','td:nth-child(2)','td.lAlign > a','','href')
    U.getData(driver,"tbody > tr")

    B.CompareSend()
    C.CompareSend()
    K.CompareSend()
    U.CompareSend()

    driver.close()