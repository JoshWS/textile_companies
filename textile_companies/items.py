# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class TextileCompaniesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Adds company profile url
    url = scrapy.Field(output_processor=TakeFirst())

    # Adds company name
    name = scrapy.Field(output_processor=TakeFirst())

    image_url = scrapy.Field(output_processor=TakeFirst())

    address = scrapy.Field(output_processor=TakeFirst())

    township = scrapy.Field(output_processor=TakeFirst())

    phone = scrapy.Field(output_processor=TakeFirst())

    email = scrapy.Field(output_processor=TakeFirst())

    website = scrapy.Field(output_processor=TakeFirst())

    social_media_links = scrapy.Field(output_processor=TakeFirst())

    brands_and_services = scrapy.Field(output_processor=TakeFirst())

    business_categories = scrapy.Field(output_processor=TakeFirst())

    category = scrapy.Field(output_processor=TakeFirst())

    company_profile = scrapy.Field(output_processor=TakeFirst())

    # Article text with basic html preserved.
    html = scrapy.Field(output_processor=TakeFirst())
