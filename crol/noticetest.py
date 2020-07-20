import noticebot
import schedule

'''
schedule.every(5).seconds.do(noticebot.run)

while True:
    schedule.run_pending()
    noticebot.time.sleep(1)
'''

noticebot.run()
