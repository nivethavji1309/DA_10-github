import unittest
import requests
import scrapy
from scrapy.http.request import Request
url = 'https://brickset.com/sets/year-2007'
r = requests.get(url)
print(r.text)
print("Status code:")
print("\t *", r.status_code)
h = requests.head(url)
print("Header:")
print("***")
for x in h.headers:
    print("\t", x, ":", h.headers[x])
print("*****")


class DA_10(unittest.TestCase):
    headers = {'User-Agent': 'Android 5.0'}
    url2 = 'https://brickset.com/sets/year-2007'
    rh = requests.get(url2, headers=headers)
    print(rh.text)

    def test_headers(self):
        self.assertTrue(DA_10.headers, 'Android 5.0')

if __name__ == '__main__':
    unittest.main()

class DA_10_Spider(scrapy.Spider):
    name = 'DA_10_spider'
    start_urls = ['https://brickset.com/sets/year-2007']

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Android 7.0; Mobile; rv:54.0) Gecko/54.0 Firefox/54.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        css_selector = 'img'
        for x in response.css(css_selector):
            newsel = '@src'
            yield {'Image Link': x.xpath(newsel).extract_first(),}

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        headers = {'User-Agent': 'Mozilla/5.0 (Android 7.0; Mobile; rv:54.0) Gecko/54.0 Firefox/54.0'}
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse,
                headers= headers)
