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

    # Adds image url
    image_url = scrapy.Field(output_processor=TakeFirst())

    # Adds address
    address = scrapy.Field(output_processor=TakeFirst())

    # Adds township
    township = scrapy.Field(output_processor=TakeFirst())

    # Adds phone number
    phone_number = scrapy.Field(output_processor=TakeFirst())

    # Adds email
    email = scrapy.Field(output_processor=TakeFirst())

    # Adds website url
    website_url = scrapy.Field(output_processor=TakeFirst())

    # Adds social media links
    social_media_links = scrapy.Field(output_processor=TakeFirst())

    # Adds brands and services
    brands_and_services = scrapy.Field(output_processor=TakeFirst())

    # Adds business categories
    business_categories = scrapy.Field(output_processor=TakeFirst())

    # Adds category
    category = scrapy.Field(output_processor=TakeFirst())

    # Adds company profile
    company_profile = scrapy.Field(output_processor=TakeFirst())
