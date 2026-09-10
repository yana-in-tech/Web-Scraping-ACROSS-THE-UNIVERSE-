import asyncio
from playwright.async_api import async_playwright


URL: str = “https://dog.com" #good boy example 
async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(URL, wait_until="networkidle")

        #article h2 is just example selector
        #for item in soup.select("div.article-card"):
        #   title = item.select_one("h2")
        titles = await page.locator("article h2").all_text_contents()
        print(titles)

        await browser.close()

asyncio.run(scrape())

