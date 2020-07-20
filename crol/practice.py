import sqlite3
################################################################################################
################################################################################################
################################################################################################
############################## FORMER CODE #####################################################
################################################################################################
################################################################################################
################################################################################################

con=sqlite3.connect("crol/noticedb2.sqlite")

cur= con.cursor()
'''
cur.execute("drop table notice_upbit")
cur.execute("drop table notice_bithumb")
cur.execute("drop table notice_coinone")
cur.execute("drop table notice_korbit")
'''

'''
cur.execute("select * from notice_upbit")
for i in cur:
    print(i)
cur.execute("select * from notice_bithumb")
for i in cur:
    print(i)
cur.execute("select * from notice_coinone")
for i in cur:
    print(i)
cur.execute("select * from notice_korbit")
for i in cur:
    print(i)
'''

cur.execute("CREATE TABLE notices(TITLE text, DATE text, LINK text, EXCHANGE text, CREATED text)")




con.close()