import aiohttp
import asyncio
from parsel import Selector
import json

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

def printProduct(item, media) :
    price = item['price']
    img = 'https://static.zara.net/photos///{}/w/560/{}.jpg?ts={}'.format(media['path'], media['name'],
                                                                          media['timestamp'])
    print('price: ' + str(price))
    print('img url: ' + img)

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://search.daum.net/search?q=환율')
        selector = Selector(html)
        currencies = selector.xpath('//div[@id="exBoxTab"]/a/span[@class="inner_tit"]/text()').re(r'원/s*(.*)')
        exchanges = selector.xpath('//div[@id="exBoxTab"]/a/span/em[@class="txt_num"]/text()').getall()
        for index, currency in enumerate(currencies):
            print(currency, exchanges[index])

    keyword = 'BEIGE-6318/234'
    url = 'https://api.empathybroker.com/search/v1/query/zara/search?lang=en_GB&store=20701&warehouse=30551&q='
    async with aiohttp.ClientSession() as session:
        obj = json.loads(await fetch(session, url + keyword))
        if(obj['numFound'] > 0):
            printProduct(obj['products'][0], obj['products'][0]['xmedia'][0])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as ex:
        print(ex)