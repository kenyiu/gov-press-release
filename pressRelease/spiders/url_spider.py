from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from pressRelease.items import *
from scrapy.http import Request
import re
import urlparse

class UrlSpider(BaseSpider):
	name = "url"
	# allowed_domains = ["http://www.info.gov.hk"]

	def start_requests(self):
		for year in range(2007, 2016):
			for month in range(1, 13):
				for day in range(1, 32):
					yield self.make_requests_from_url("http://www.info.gov.hk/gia/general/%04d%02d/%02dc.htm" %(year, month, day))

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath('//ul[@id="prlist"]/li')
		datetime = ''.join(sel.select('//h2[@id="date"]/text()').extract());
		datetime = datetime.split('-')
		datetime = datetime[2]+"-"+datetime[1]+"-"+datetime[0]
		items = []

		for site in sites:
			item = PressreleaseItem()
			url = ''.join(site.xpath('a/@href').extract())
			if re.match('^/', url):
				url = "http://www.info.gov.hk/"+url

			if not re.match('^http', url):
				url = urlparse.urljoin(response.url, url)

			title = ''.join(site.xpath('a/text()').extract())
			request = Request(url=url, callback=self.parse_content)
			request.meta['item'] = item
			request.meta['url'] = url
			request.meta['title'] = title
			request.meta['datetime'] = datetime
			yield request
			
	def parse_content(self, response):
		item = response.meta['item']
		item['title'] = response.meta['title']
		item['url'] = response.meta['url']
		item['datetime'] = response.meta['datetime']

		sel = Selector(response)

		item['content'] = ''.join(sel.select('//div[@id="pressrelease"]/p').extract()).replace(" ", "")
		
		yield item