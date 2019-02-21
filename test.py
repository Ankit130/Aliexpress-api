import requests
from openpyxl import load_workbook
from bs4 import BeautifulSoup as soup
import time
import csv
import urllib
wb=load_workbook('links.xlsx')
sht=wb.active
url=input("Enter url of Product: ")
plists=[]
try:
    r=requests.get(url)
except:
    print("Error in script")
Soup=soup(r.text,'html.parser')
name=Soup.find('h1',attrs={'class':'product-name'}).text.strip().encode('utf-8')
try:
    brand=Soup.find('li',attrs={'id':'product-prop-2'}).get('data-title').encode('utf-8')
except:
    brand=''
desc=''
dess=Soup.findAll('li',attrs={'id':'product-prop-'})
for des in dess:
    desc1=des.findAll('span')
    desc=desc+desc1[0].text.strip().encode('utf-8')+" "+desc1[1].text.strip().encode('utf-8')+"\n"
weight=''
dime=''
pack=Soup.find('ul',attrs={'class':'product-packaging-list util-clearfix'})
lis=pack.findAll('li')
for li in lis:
   spans= li.findAll('span')
   key=spans[0].text.strip().encode('utf-8')
   if key=='Package Weight:':
       weight=spans[1].text.strip().encode('utf-8')
       continue
   if key=='Package Size:':
       dime=spans[1].text.strip().encode('utf-8')
       continue
try:
    mat=Soup.find('li',attrs={'id':'product-prop-10'}).get('data-title').encode('utf-8')
except:
    mat=''
try:
    price=Soup.find('del',attrs={'class':'p-del-price-content notranslate'}).text.encode('utf-8').strip()
except:
    price=''
try:
    sprice=Soup.find('div',attrs={'class':'p-price-content notranslate'}).text.encode('utf-8').strip()
except:
    sprice=''
tech=''
lis=Soup.findAll('li',attrs={'class':'property-item'})
for li in lis:
    spans=li.findAll('span')
    tech=tech+spans[0].text.encode('utf-8').strip()+" "
    tech=tech+spans[1].text.encode('utf-8').strip()+ '\n'
try:
    warranty=Soup.find('dl',attrs={'id':'serve-guarantees-detail'}).text.encode('utf-8').replace('Seller Guarantees:','').strip()
except:
    warranty=''
try:
    returnp=Soup.find('dl',attrs={'class':'return-policy util-clearfix'}).text.encode('utf-8').replace('Return Policy','').strip()
except:
    returnp=''
cat=''
divs=Soup.find('div',attrs={'class':'container'})
aa=divs.findAll('a')
try:
    cat=aa[len(aa)-1].get('title')
except:
    pass
plist.append(cat)
ul=Soup.find('ul',attrs={'id':'j-image-thumb-list'})
lis=ul.findAll('li')
imgs=[]
for li in lis:
    try:
        img_url=li.find('img').get('src').replace('_50x50.jpeg','').replace('_50x50.jpg','')
        imgs.append(img_url)
    except:
        break
dict={'Product Name':name,
      'Brand':brand,
      'description':desc,
      'Weight':weight,
      'Dimension':dime,
      'Material':mat,
      'Price':price,
      'Special Price':sprice,
      'Technical Detail':tech,
      'Warranty':warranty,
      'Return Policy':returnp,
      'Image Urls':imgs
     }

print(dict)




