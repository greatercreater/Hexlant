import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime, date, timedelta
import sqlite3
import telegram
################################################################################################
################################################################################################
################################################################################################
############################## FORMER CODE #####################################################
################################################################################################
################################################################################################
################################################################################################

class Notice:
    
    def __init__(self):
        self.title=[]
        self.dates=[]
        self.link=[]
        self.arr=dict()
    
    # Compare data in DB and data in server to return index and type of new data
    def CompareandSet(self, exchange):
        # Get data in DB
        con=sqlite3.connect("crol/crol_db.sqlite")
        cur=con.cursor()
        cur.execute("select * from notice_"+exchange)
        #store in list
        Indb=list(cur.fetchall())
        con.close()

        # Compare data
        arr=dict()
        n=len(self.link)-1
        if len(Indb) <= n:
                print("이상이상"+exchange)
                print("Indb: ",len(Indb))
                print("n: ",n)
                exit(1)
        else:
            pass
        
        while n>=0:
            #distinguish new one and modified one
            for i in Indb:
                if (self.link[n]==i[2]) and (self.title[n]==i[0]):
                    break
                elif self.link[n]==i[2] and not self.title[n]==i[0]:
                    arr[n]="mod"
                    break
                else:
                    continue
            else:
                arr[n]="new"
            
            n-=1
        
        return arr


    # Send message to a telegram channel and update new data on DB
    def send2U(self,exchange):
        my_token='1339037346:AAHOFfZQZb5qqRV_xacyyVyhQb9-qaXWIFE'

        bot=telegram.Bot(token=my_token)
        id=-1001472766381  #channel id 
        

        #send messages and update on db
        cur_time=datetime.now().strftime("%c")
        con=sqlite3.connect("crol/crol_db.sqlite")
        cur=con.cursor()
        for a in self.arr:
            bot.sendMessage(chat_id=id, text="<b>"+exchange+"</b>\n"+self.title[a]+"\n\nUpload Date: "+self.dates[a]+"\n\n"+self.link[a], parse_mode='HTML')
            
            if self.arr[a]=="new":
                pass
                cur.execute("insert into notice_"+exchange+" values(?,?,?,?,?,?)",(self.title[a],self.dates[a],self.link[a],exchange,cur_time,''))
            elif self.arr[a]=="mod":
                pass
                cur.execute("update notice_"+exchange+" set TITLE = ?, DB_MODIFIED = ? where LINK = ?",(self.title[a],cur_time,self.link[a]))
            else:
                print("이상이상2")
                exit(1)
                break
        
        con.commit()
        con.close()
    


    def GetUpbit(self,driver):
        uurl='https://upbit.com/service_center/notice'
        driver.get(uurl)

        time.sleep(6)
        source=driver.page_source
        u_ttemp=driver.find_element_by_tag_name('tbody tr').find_elements_by_xpath('//td[1]')  #temporary title
        u_dtemp=driver.find_element_by_tag_name('tbody tr').find_elements_by_xpath('//td[2]')  #temporary date

        soup=BeautifulSoup(source, 'html.parser')
        u_temp=soup.select('tbody tr td a')  #temporary link
        u_emBlue=soup.select('tbody tr.emBlue td.lAlign')  #do not update this info
        u_top=soup.select('tbody tr.top td.lAlign')  #do not update this info

        u_length=0
       
        #store as a list strings
        for j in u_temp:
            self.link.append(j.get('href'))
        for j in u_ttemp:
            self.title.append(j.text)
        for j in u_dtemp:
            self.dates.append(j.text)
            u_length+=1

        #except u_emblue and u_top
        n=0
        for j in u_emBlue:
            self.title.remove(j.text)
            self.link.pop(0)
            n+=1
        
        n=0
        for j in u_top:
            self.title.pop(0)
            self.dates.pop(0)
            self.link.pop(0)
            n+=1
        u_length-=n

        #complete links
        base_board='https://upbit.com'
        i=0
        while i<u_length:
            self.link[i]=base_board+self.link[i]
            i+=1



    def GetBithumb(self,driver):
        burl='https://cafe.bithumb.com/view/boards/43'
        driver.get(burl)

        time.sleep(2)
        source=driver.page_source
        soup=BeautifulSoup(source, 'html.parser')
        self.title=soup.select("tbody tr[style*='white'] td.one-line")
        self.dates=soup.select("tbody tr[style*='white'] td.small-size")[1::2]

        #store title and date
        b_length=0
        for j in self.dates:
            b_length+=1
        for i in range(b_length):
            self.dates[i]=self.dates[i].text
            self.title[i]=self.title[i].text

        #change time to date, ex)14:30->2020.01.01
        now=datetime.now()
        i=0
        for j in self.dates:
            if(j.find(":")==-1):
                i+=1
                continue
            else:
                if int(j[1:3])>now.hour:
                    yesterday=date.today()-timedelta(1)
                    self.dates[i]=yesterday.strftime('%Y.%m.%d')
                elif int(j[1:3])<now.hour:
                    self.dates[i]=date.today().strftime('%Y.%m.%d')
                else:
                    if int(j[4:6])>now.minute:
                        yesterday=date.today()-timedelta(1)
                        self.dates[i]=yesterday.strftime('%Y.%m.%d')
                    else:
                        self.dates[i]=date.today().strftime('%Y.%m.%d')
                i+=1

        #except fixed notices
        b_temp=soup.select("tbody tr[style*='white']")
        string=''

        for j in b_temp:
            string=(j.get('onclick'))[15:22]
            self.link.append(string)

        #complete links
        base_board='https://cafe.bithumb.com/view/board-contents/'

        i=0
        while i<b_length:
            self.link[i]=base_board+self.link[i]
            i+=1


        
    def GetCoinone(self,driver):
        curl='https://coinone.co.kr'
        driver.get(curl)

        time.sleep(6)
        source=driver.page_source
        soup=BeautifulSoup(source, 'html.parser')

        self.title=soup.select('div.pc-notice-dropdown .notice-title')
        self.dates=soup.select('div.pc-notice-dropdown .notice-date')

        c_temp=soup.select('div.pc-notice-dropdown a.notice-link')
        c_length=0
        for j in c_temp:
            self.link.append(j.get('href'))
            c_length+=1

        i=0
        while i<c_length:
            self.link[i]=curl+self.link[i]
            self.title[i]=(self.title[i].text).lstrip()
            self.dates[i]=self.dates[i].text
            i+=1


    def GetKorbit(self):
        kurl='https://korbitblog.tumblr.com/'

        source=requests.get(kurl)
        soup=BeautifulSoup(source.text, 'html.parser')

        #get title and date
        self.title=soup.select('h1 a')
        k_dtemp=soup.select('a time')
        k_length=0
        for j in k_dtemp:
            self.dates.append(j.get('datetime'))
            k_length+=1

        #convert 2020-01-01 to 2020.01.01
        i=0
        while i<k_length:
            self.dates[i]=(self.dates[i])[:10]
            self.dates[i]=(self.dates[i]).replace("-",".")
            i+=1

        #get links
        k_temp=self.title
        for j in k_temp:
            self.link.append(j.get('href'))

        for i in range(k_length):
            self.title[i]=self.title[i].text
        


    # Major function// get and compare and set new notices
    def GetandCompareandSet(self):
        driver= webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')

        self.GetUpbit(driver)
        self.arr=self.CompareandSet("upbit")
        self.send2U("upbit")
        
        self.__init__()
        self.GetBithumb(driver)
        self.arr=self.CompareandSet("bithumb")
        self.send2U("bithumb")
        
        self.__init__()
        self.GetCoinone(driver)
        self.arr=self.CompareandSet("coinone")
        self.send2U("coinone")
        
        self.__init__()
        self.GetKorbit()
        self.arr=self.CompareandSet("korbit")
        self.send2U("korbit")

        self.__init__()
        driver.quit()