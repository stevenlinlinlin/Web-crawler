from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import requests

area_city_url = []
with open('area_city_url.txt', 'r', newline='') as f:
    city = f.readlines()
    for c in city:
        area_city_url.append(c.strip('\n'))
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
        
        await stealth(page=page)
    
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

#print(area_new_restaurants)
