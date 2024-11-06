import requests

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError


class PageResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content


class RequestStrategy:
    def __init__(self):
        pass

    def meta_redirect(self, content):
        soup = BeautifulSoup(content)

        result = soup.find_all(
            "meta", attrs={"http-equiv": "refresh"}
        ) + soup.find_all("meta", attrs={"http-equiv": "Refresh"})
        if len(result) > 0:
            meta_tag_content_val = result[0]["content"].split(";")
            if len(meta_tag_content_val) > 1:
                return meta_tag_content_val[1].strip().lower()
            else:
                return None
        return None

    def scrape(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "referer": "httpbin.org",
            "Dnt": "1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Proxy-Connection": "keep-alive",
        }
        response = requests.get(url, headers=headers)
        while self.meta_redirect(response.content):
            url = self.meta_redirect(response.content)
            response = requests.get(url, headers=headers)

        return PageResponse(response.status_code, response.content)


class PlaywrightStrategy:
    def __init__(self):
        pass

    async def scrape(self, url):
        response = PageResponse(400, "")
        async with async_playwright() as p:
            for browser_type in [p.chromium, p.firefox, p.webkit]:
                browser = await browser_type.launch()
                agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                headers = {
                    "referer": "httpbin.org",
                    "Dnt": "1",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept": "*/*",
                }
                context = await browser.new_context(
                    user_agent=agent,
                    color_scheme=r"light",
                    locale=r"en-US,en;q=0.9",
                    extra_http_headers=headers,
                )
                page = await context.new_page()
                try:
                    result = await page.goto(url)
                    # page.screenshot(path=f'example-{browser_type.name}.png') # Future uses may require screenshots
                    response = PageResponse(
                        result.status, await page.content()
                    )
                except TimeoutError:
                    if len(await page.content()) > 0:
                        response = PageResponse(200, await page.content())
                    else:
                        response = PageResponse(500, "No content")
                await browser.close()

        return response


class WebScraper:
    def __init__(self, strategy=PlaywrightStrategy()):
        self.strategy = strategy

    def scrape(self, url):
        return self.strategy.scrape(url)
