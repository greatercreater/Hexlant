from django.db import models
from selenium import webdriver


driver= webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')
url='https://upbit.com/service_center/notice'
driver.get(url)
driver.implicitly_wait(5)
source=driver.page_source
content=driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

#driver.quit()
#//*[@id="UpbitLayout"]/div[3]/div/section[2]/article/div/div[2]/table/tbody/tr[5]/td[2]
#//*[@id="UpbitLayout"]/div[3]/div/section[2]/article/div/div[2]/table/tbody/tr[5]/td[1]/a
#//*[@id="UpbitLayout"]/div[3]/div/section[2]/article/div/div[2]/table/tbody/tr[5]/td[3]

print(content[1].text)

# Create your models here.
class Page(models.Model):
    title= models.CharField(max_length=20)
    notices=content[4:]
    top=content[0]
    guide=content[1:4]
    
