import scrapy
from scrapy.loader import ItemLoader
from textile_companies.items import TextileCompaniesItem


class TextileCompaniesMyanmarSpider(scrapy.Spider):
    name = "textilemyanmar"
    allowed_domains = [
        "www.textiledirectory.com.mm",
    ]
    start_urls = [
        "https://www.textiledirectory.com.mm/categories/dyeing/chemicals.html?q=Chemicals"
    ]

    def parse(self, response):
        # Follow links to company profiles
        companies = response.xpath(
            "//a[contains(@class, 'btn btn-lg btn-block')]/@href"
        )
        for company in companies:
            yield response.follow(company, self.parse_company)

        # follow pagination links
        next_page = response.xpath("//a[@title='Next']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_company(self, response):
        l = ItemLoader(item=TextileCompaniesItem(), response=response)

        l.add_value("url", response.url)

        return l.load_item()
