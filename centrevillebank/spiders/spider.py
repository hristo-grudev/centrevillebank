import scrapy

from scrapy.loader import ItemLoader

from ..items import CentrevillebankItem
from itemloaders.processors import TakeFirst


class CentrevillebankSpider(scrapy.Spider):
	name = 'centrevillebank'
	start_urls = ['https://www.centrevillebank.com/About/Who-We-Are/News']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="subpage__title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-lg-10 offset-lg-1"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="masthead__sub"]/text()').get()

		item = ItemLoader(item=CentrevillebankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
