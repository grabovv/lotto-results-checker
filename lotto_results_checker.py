import asyncio
from pyppeteer import launch
import json
from bs4 import BeautifulSoup
import lxml

def parse_html_to_json(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    pre_tag = soup.find('pre')
    if pre_tag:
        json_data = json.loads(pre_tag.text)
        return json_data
    else:
        raise ValueError("No <pre> tag found in the HTML content.")

async def main():
    url = 'https://www.lotto.pl/api/lotteries/draw-results/last-results-per-game?gameType=Lotto'
    result_html = await get_lotto_data(url)
    result_json = parse_html_to_json(result_html)

    draw_data = result_json[0]
    draw_date = draw_data['drawDate']
    lotto_results = draw_data['results'][0]['resultsJson']
    lotto_plus_results = draw_data['results'][1]['resultsJson']
    
    print(f"Data losowania: {draw_date}")
    print(f"Wyniki Lotto: {lotto_results}")
    print(f"Wyniki Lotto Plus: {lotto_plus_results}")

async def get_lotto_data(url):
    browser = await launch(headless=True, executablePath='<path_to_chrome_binary>')
    
    try:
        page = await browser.newPage()
        await page.setExtraHTTPHeaders({
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
        })
        await page.goto(url)
        await page.waitForSelector('body')
        page_content = await page.content()
        return page_content
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
