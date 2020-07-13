import crollll
import schedule


schedule.every(4).minutes.do(crollll.GetandCompareandSet)

while True:
    schedule.run_pending()
    crollll.time.sleep(1)
'''
crollll.GetandCompareandSet()
'''
