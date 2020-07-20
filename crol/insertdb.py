import noticebot

    
    

if __name__=='__main__':
    driver= noticebot.webdriver.Chrome('C:/chromedriver_win32/chromedriver')
    noticebot.time.sleep(1)
    B=noticebot.Exchanger(0,'https://cafe.bithumb.com/view/boards/43','https://cafe.bithumb.com/view/board-contents/',"td.one-line","td:nth-child(3)",'','','onclick')
    B.getData(driver,"tbody > tr")
    C=noticebot.Exchanger(1,'https://coinone.co.kr','https://coinone.co.kr','a > div > p.info-title > span','a > span','a','','href')
    C.getData(driver,'div.crypto-info > landing-main-notice-info > ul > li')
    K=noticebot.Exchanger(2,'https://korbitblog.tumblr.com/','','h1 > a','a.post-date time','h1 > a','datetime','href')
    K.getData(driver,"div.posts.cf > article.post.post-text")
    U=noticebot.Exchanger(3,'https://upbit.com/service_center/notice','https://upbit.com','td.lAlign > a','td:nth-child(2)','td.lAlign > a','','href')
    U.getData(driver,"tbody > tr")
    
    cur_time=noticebot.datetime.now().strftime("%c")
    con=noticebot.sqlite3.connect("crol/noticedb2.sqlite")
    cur= con.cursor()

    for i in B.noticeset:
        cur.execute("insert into notices values (?,?,?,?,?)",(i.title, i.day, i.link, 'bithumb',cur_time))
    for i in C.noticeset:
        cur.execute("insert into notices values (?,?,?,?,?)",(i.title, i.day, i.link, 'coinone',cur_time))
    for i in K.noticeset:
        cur.execute("insert into notices values (?,?,?,?,?)",(i.title, i.day, i.link, 'korbit',cur_time))
    for i in U.noticeset:
        cur.execute("insert into notices values (?,?,?,?,?)",(i.title, i.day, i.link, 'upbit',cur_time))

    con.commit()
    con.close()
    
    
    
    
    
    
    
    # print("@@@@@@@@@@@@@@bithumb@@@@@@@@@@@@@@@@@@@")
    # for i in B.dataset:
    #     print(i.title)
    #     print(i.day)
    #     print(i.link)
    # print("@@@@@@@@@@@@@@coinone@@@@@@@@@@@@@@@@@@@")
    # for i in C.dataset:
    #      print(i.title)
    #      print(i.day)
    #      print(i.link)
    # print("@@@@@@@@@@@@@@korbit@@@@@@@@@@@@@@@@@@@")
    # for i in K.dataset:
    #     print(i.title)
    #     print(i.day)
    #     print(i.link)
    # print("@@@@@@@@@@@@@@upbit@@@@@@@@@@@@@@@@@@@")
    # for i in U.dataset:
    #     print(i.title)
    #     print(i.day)
    #     print(i.link)
    
    driver.close()
