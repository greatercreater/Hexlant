import requests
import csv
from django.db import models
from bs4 import BeautifulSoup

source = requests.get("https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EA%B2%8C%EC%9E%84+%EC%88%9C%EC%9C%84").text
soup = BeautifulSoup(source, "html.parser")
hotKeys = soup.select("span.tit")

f= open("C:/Users/세환/SolSource/hanbit_media/book_list.csv",'r',encoding="UTF8")
rdr=csv.reader(f)



# Create your models here.
class Board(models.Model):
    title =models.CharField(max_length=30)
    content=models.TextField()
    abc=rdr
    write_date=models.DateTimeField(auto_now_add=True)

