from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import requests

import time
from tqdm import tqdm
area_city_url = ['https://www.foodpanda.com.tw/city/changhua-county/area/changhua-city',
                 'https://www.foodpanda.com.tw/city/hsinchu-county/area/zhubei-city',
                 'https://www.foodpanda.com.tw/city/kaohsiung-city/area/cijin',
                 'https://www.foodpanda.com.tw/city/kaohsiung-city/area/fongshan',
                 'https://www.foodpanda.com.tw/city/kaohsiung-city/area/gushan',
                 'https://www.foodpanda.com.tw/city/kaohsiung-city/area/meinong',
                 'https://www.foodpanda.com.tw/city/kaohsiung-city/area/qianzhen',
                 'https://www.foodpanda.com.tw/city/kaohsiung-city/area/xiaogang',
                 'https://www.foodpanda.com.tw/city/kaohsiung-city/area/yancheng',
                 'https://www.foodpanda.com.tw/city/kaohsiung-city/area/zuoying',
                 'https://www.foodpanda.com.tw/city/miaoli-county/area/miaoli-city',
                 'https://www.foodpanda.com.tw/city/nantou-county/area/yuchi',
                 'https://www.foodpanda.com.tw/city/nantou-county/area/yuchi-sun-moon-lake',
                 'https://www.foodpanda.com.tw/city/nantou-county/area/zhushan',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/banqiao',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/danshui',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/linkou',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/sanxia',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/tucheng',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/wulai',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/xindian',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/xizhi',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/yonhe',
                 'https://www.foodpanda.com.tw/city/new-taipei-city/area/zhonghe',
                 'https://www.foodpanda.com.tw/city/pingtung-county/area/henchun',
                 'https://www.foodpanda.com.tw/city/pingtung-county/area/henchun-kenting',
                 'https://www.foodpanda.com.tw/city/pingtung-county/area/pingtung-city',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/beitun',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/dadu',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/dajia',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/dali',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/fengyuan',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/nantun',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/qingshui',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/taiping',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/west',
                 'https://www.foodpanda.com.tw/city/taichung-city/area/xitun',
                 'https://www.foodpanda.com.tw/city/tainan-city/area/annan',
                 'https://www.foodpanda.com.tw/city/tainan-city/area/anping',
                 'https://www.foodpanda.com.tw/city/tainan-city/area/east',
                 'https://www.foodpanda.com.tw/city/tainan-city/area/north',
                 'https://www.foodpanda.com.tw/city/tainan-city/area/south',
                 'https://www.foodpanda.com.tw/city/tainan-city/area/west-central',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/beitou',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/daan',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/daan-east',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/datong',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/datong-dadaocheng',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/nangang',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/neihu',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/shilin',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/songshan',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/wanhua',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/wanhua-ximending',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/wenshan',
                 'https://www.foodpanda.com.tw/city/taipei-city/area/xinyi',
                 'https://www.foodpanda.com.tw/city/taitung-county/area/chenggong',
                 'https://www.foodpanda.com.tw/city/taitung-county/area/donghe',
                 'https://www.foodpanda.com.tw/city/taitung-county/area/dulan',
                 'https://www.foodpanda.com.tw/city/taitung-county/area/taimali',
                 'https://www.foodpanda.com.tw/city/taitung-county/area/taitung-city',
                 'https://www.foodpanda.com.tw/city/taoyuan-city/area/longtan',
                 'https://www.foodpanda.com.tw/city/taoyuan-city/area/zhongli',
                 'https://www.foodpanda.com.tw/city/yilan-county/area/jiaoxi',
                 'https://www.foodpanda.com.tw/city/yilan-county/area/luodong',
                 'https://www.foodpanda.com.tw/city/yilan-county/area/yilan-city',
                 'https://www.foodpanda.com.tw/city/yunlin-county/area/douliu-city']

urls = area_city_url[14]
# headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
# ip = '31.186.239.244:8080'
# res = requests.get('https://api.ipify.org?format=json',
#                    proxies={'http': ip, 'https': ip}, timeout=5)
# print(res.json())

def find_new_restaurants(doc):
    soup = BeautifulSoup(doc, 'lxml')

    #print(soup.prettify())
    with open(f"foodpanda.html", 'w') as f:
        f.write(soup.prettify())

    page_new_restaurants = []
    restaurants = soup.find_all('li', class_='vendor-tile-wrapper')
    print(len(restaurants))
    
    for restaurant in restaurants:
        tag = restaurant.find('div', class_='multi-tag')
        if tag and tag.getText() == '超人氣餐廳':  # '新上線':
            newrestaurant = restaurant.find('a', class_='name fn').getText()
            #print(tag.getText())
            page_new_restaurants.append(newrestaurant)
            
    return page_new_restaurants


async def main():
    browser = await launch(headless=True)#, args=[f'--proxy-server={ip}'])
    results = []
    for i in range(1, 5):
        page = await browser.newPage()
        await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36')
        
        await stealth(page=page)  # <-- Here
    
    # results = []
    # for i in range(1, 5):
        url = urls + f"?page={i}"
        await page.goto(url)
        await page.waitFor(i * 1000)
        
        # await page.waitFor(5000)
        # await page.evaluate("""{window.scrollBy(0, document.body.scrollHeight);}""")
        
        doc = await page.content()
        page_new_restaurants = find_new_restaurants(doc)
        results.append(restaurant for restaurant in page_new_restaurants)
        
    await page.screenshot({'path': 'foodpanda.png'})

    await browser.close()
    return results

area_new_restaurants = asyncio.get_event_loop().run_until_complete(main())

print(area_new_restaurants)
