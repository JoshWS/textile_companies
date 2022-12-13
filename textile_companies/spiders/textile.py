import scrapy
from scrapy.loader import ItemLoader
from textile_companies.items import TextileCompaniesItem
from itemloaders.processors import Join


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

        # # follow pagination links
        # next_page = response.xpath("//a[@title='Next']/@href").extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_company(self, response):
        l = ItemLoader(item=TextileCompaniesItem(), response=response)

        # Variables with all xpaths
        name = "//meta[@property='og:title']/@content"
        image_url = "//div[@class='item active']/a/@href"
        address = "//dd[1]/text() | //div[@class='address'][2]/p/text()"
        township = "//dd[2]/text()"
        phone_number = "//dd[3]//a/text() | //div[@class='address'][3]//a/text()"
        # email =
        # website_url =
        # social_media_links =
        # brands_and_services =
        # business_categories =
        # category =
        # company_profile =
        # page_html =
        # Adds company profile url
        l.add_value("url", response.url)

        # Adds company name
        l.add_xpath(
            "name",
            name,
        )

        # Adds image url
        if l.get_xpath(image_url):
            l.add_xpath("image_url", image_url)

        # Adds address
        l.add_xpath("address", address)

        # Adds township
        if l.get_xpath(township):
            l.add_xpath("township", township)
        # Adds phone number
        l.add_xpath("phone_number", phone_number, Join(""))
        # Adds email

        # Adds website url

        # Adds social media links

        # Adds brands and services

        # Adds business categories

        # Adds category

        # Adds company profile

        # Adds page html

        return l.load_item()
