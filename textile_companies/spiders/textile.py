import scrapy
from scrapy.loader import ItemLoader
from textile_companies.items import TextileCompaniesItem
from itemloaders.processors import Join


def decode_email(encoded_string):
    r = int(encoded_string[:2], 16)
    email = "".join(
        [
            chr(int(encoded_string[i : i + 2], 16) ^ r)
            for i in range(2, len(encoded_string), 2)
        ]
    )
    return email


class TextileCompaniesMyanmarSpider(scrapy.Spider):
    name = "textilemyanmar"
    allowed_domains = [
        "www.textiledirectory.com.mm",
    ]
    start_urls = [
        "https://www.textiledirectory.com.mm/categories/dyeing/chemicals.html?q=Chemicals",
        "https://www.textiledirectory.com.mm/categories/dyeing/dyeing-printing-textiles.html?q=Dyeing%20&Printing_Textiles=",
        "https://www.textiledirectory.com.mm/categories/dyeing/dyes.html?q=Dyes",
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
        email = "//dd[4]//span/@data-cfemail"
        website_url = "//label[contains(text(), 'Website')]/../p/a/text() | //dl[@class='dl-horizontal']//a[@rel='nofollow']/text()"
        social_media_links = "//a[@title='Facebook']/@href"
        # brands_and_services =
        # business_categories =
        # category =
        # company_profile =
        # page_html =
        # Adds company profile url

        l.add_value("url", response.url)

        # Adds company name
        l.add_xpath("name", name)

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
        if l.get_xpath(email[0]):
            l.add_value("email", decode_email(email))

        # Adds website url
        if l.get_xpath(website_url):
            l.add_xpath("website_url", website_url)

        # Adds social media links
        if l.get_xpath(social_media_links):
            l.add_xpath("social_media_links", social_media_links)

        # Adds brands and services

        # Adds business categories

        # Adds category

        # Adds company profile

        # Adds page html

        return l.load_item()
