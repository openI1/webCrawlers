import requests
from bs4 import BeautifulSoup
import xlwt

url='https://editorial.rottentomatoes.com/guide/best-new-movies/'

def getResponse(url):
    try:
        response=requests.get(url)
        if(response.status_code==200):
            return response.text
    except requests.RequestException:
        return None
list=[]
n=1
soup = BeautifulSoup(getResponse(url),'lxml')

book=xlwt.Workbook(encoding='utf-8',style_compression=0)

sheet=book.add_sheet('Best_movies_2024_RT',cell_overwrite_ok=True)
sheet.write(0,0,'article_movie_title')
sheet.write(0,1,'tMeterScore')
sheet.write(0,2,'Critics Consensus')
sheet.write(0,3,'Starring')
sheet.write(0,4,'Directed By')
for num in range(1,101):
    list+=soup.find_all(id=f'row-index-{num}',limit=1)
for item in list:
    sheet.write(n,0,item.find(class_='article_movie_title').find("a").string)
    sheet.write(n,1,item.find(class_='tMeterScore').string)
    sheet.write(n,2,item.find(class_='info critics-consensus').get_text(strip=True))
    sti=''
    for i in item.find(class_='info cast').find_all('a'):
        sti=sti+i.text+'  '
    sheet.write(n,3,sti)
    for j in item.find(class_='info director').find_all("a"):
        sti=sti+j.text+'  '
    sheet.write(n,4,j.text)
    n+=1


book.save(u'Best_movies_2024_RT.xls')