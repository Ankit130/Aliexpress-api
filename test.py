import requests
from openpyxl import load_workbook
from bs4 import BeautifulSoup as soup
import time
import csv
import urllib
wb=load_workbook('links.xlsx')
sht=wb.active
#url='https://www.aliexpress.com/category/200215377/figurines-miniatures/'
plists=[]

i=1
while i<500:
    time.sleep(2)
    print i
    plist=[]
    time.sleep(2)
    #url='https://www.aliexpress.com/category/200215377/figurines-miniatures/'+str(page)+'.html?spm=2114.11010108.107.11.650c649bLl3wCa'
    #url='https://www.aliexpress.com/category/200215377/figurines-miniatures/'+str(page)+'.html?site=glo&g=y&needQuery=n&tag='
    #url='https://www.aliexpress.com/category/152805/wall-clocks.'+str(page)+'html?spm=2114.11010108.107.12.650c649bLl3wCa'
    #url='https://www.aliexpress.com/category/40503/cushion.'+str(page)+'html?spm=2114.11010108.107.14.650c649bLl3wCa'
    #url='https://www.aliexpress.com/category/100004864/storage-boxes-bins'+str(page)+'.html?spm=2114.11010108.107.24.650c649bLl3wCa'
    #url='https://www.aliexpress.com/category/200215653/drawer-organizers'+str(page)+'.html?spm=2114.11010108.107.26.650c649bLl3wCa'
    #url='https://www.aliexpress.com/category/150303/home-furniture'+str(page)+'.html?spm=2114.11010108.107.44.650c649bLl3wCa'
    url= sht['A'+str(i)].value
    try:
        r=requests.get(url)
        print "jg"
    except:
        break
    Soup=soup(r.text,'html.parser')
    name=Soup.find('h1',attrs={'class':'product-name'}).text.strip().encode('utf-8')
    plist.append(url)
    plist.append(name)
    print name
    try:
        brand=Soup.find('li',attrs={'id':'product-prop-2'}).get('data-title').encode('utf-8')
    except:
        brand=''
    plist.append(brand)
    desc=''
    dess=Soup.findAll('li',attrs={'id':'product-prop-'})
    for des in dess:
        desc1=des.findAll('span')
        desc=desc+desc1[0].text.strip().encode('utf-8')+" "+desc1[1].text.strip().encode('utf-8')+"\n"
    plist.append(desc)
    print desc
    '''
    dimgs=[]
    count=0
    dname='desc-'+str(i)+'-'
    div=Soup.find('div',attrs={'id':'j-product-description'})
    ps=div.findAll('p')
    for p in ps:
        dimgs1=p.findAll('img')
        if len(dimgs1)==0:
            continue
        else:
            for dm in dimgs1:
                if len(dimgs)>5:
                    break
                img_url=dm.get('src')
                print img_url
                try:
                    r1 = requests.get(img_url)
                except:
                    print "error"
                    break
                if r1.status_code == 200:
                    count =count+1
                    with open(dname+count+'.jpg', 'wb') as f:
                        f.write(r1.content)
                        dimgs.append(dname+count+'.jpg')'''
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
    plist.append(dime)
    try:
        mat=Soup.find('li',attrs={'id':'product-prop-10'}).get('data-title').encode('utf-8')
    except:
        mat=''
    plist.append(mat)
    try:
        price=Soup.find('del',attrs={'class':'p-del-price-content notranslate'}).text.encode('utf-8').strip()
    except:
        price=''
    plist.append(price)
    try:
        sprice=Soup.find('div',attrs={'class':'p-price-content notranslate'}).text.encode('utf-8').strip()
    except:
        sprice=''
    plist.append(sprice)
    tech=''
    lis=Soup.findAll('li',attrs={'class':'property-item'})
    for li in lis:
        spans=li.findAll('span')
        tech=tech+spans[0].text.encode('utf-8').strip()+" "
        tech=tech+spans[1].text.encode('utf-8').strip()+ '\n'
    plist.append(tech)
    try:
        warranty=Soup.find('dl',attrs={'id':'serve-guarantees-detail'}).text.encode('utf-8').replace('Seller Guarantees:','').strip()
    except:
        warranty=''
    plist.append(warranty)
    try:
        returnp=Soup.find('dl',attrs={'class':'return-policy util-clearfix'}).text.encode('utf-8').replace('Return Policy','').strip()
    except:
        returnp=''
    plist.append(returnp)
    plist.append(weight)
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
    count=0
    img='pro-'+str(i)+'-'
    #for k in dimgs:
    #    plist.append(k)
    for li in lis:
        try:
            img_url=li.find('img').get('src').replace('_50x50.jpeg','').replace('_50x50.jpg','')
            print img_url
        except:
            break
        try:
                r1 = requests.get(img_url)
                print "ankit"
        except:
                print "error1"
                break
        if r1.status_code == 200:
                count =count+1
                with open(img+str(count)+'.jpg', 'wb') as f:
                    f.write(r1.content)
                    plist.append(img+str(count)+'.jpg')
    
    
    plists.append(plist)
    i=i+1
with open('output.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(plists)   
