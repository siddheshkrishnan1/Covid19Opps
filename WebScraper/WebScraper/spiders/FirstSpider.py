from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'crawlspider'
    start_urls = ['https://eureka.utexas.edu/search/projects']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = dict()
        item['url'] = response.url
        item['title'] = response.meta['link_text']
        item['body'] = '\n'.join(response.xpath('//text()').extract())
        item['source'] = response.body
        return item