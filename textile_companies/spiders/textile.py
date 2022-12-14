import scrapy
from scrapy.loader import ItemLoader
from textile_companies.items import TextileCompaniesItem
from itemloaders.processors import Join, MapCompose


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
        "https://www.textiledirectory.com.mm/categories/dyeing/chemicals.html?q=Chemicals",
        "https://www.textiledirectory.com.mm/categories/dyeing/dyeing-printing-textiles.html?q=Dyeing%20&Printing_Textiles=",
        "https://www.textiledirectory.com.mm/categories/dyeing/dyes.html?q=Dyes",
        "https://www.textiledirectory.com.mm/categories/dyeing/laundries.html?q=Laundries",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/bags.html?q=Bags",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/batik.html?q=Batik",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/bedroom-accessories.html?q=Bedroom%20Accessories",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/children-infants-wear.html?q=Children%20&Infants_Wear=",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/curtains.html?q=Curtains",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/fabric-shops.html?q=Fabric%20Shops",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/fashion-ladies-wear.html?q=Fashion%20&Ladies_Wear=",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/hat-shops.html?q=Hat%20Shops",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/men-s-wear.html?q=Men's%20Wear",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/silk-wear.html?q=Silk%20Wear",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/sports-wear.html?q=Sports%20Wear",
        "https://www.textiledirectory.com.mm/categories/fashion-textile-products/traditional-wear.html?q=Traditional%20Wear",
        "https://www.textiledirectory.com.mm/categories/garment-textile-accessories/buttons.html?q=Buttons",
        "https://www.textiledirectory.com.mm/categories/garment-textile-accessories/embroidery-machines-services.html?q=Embroidery%20Machines%20&Services=",
        "https://www.textiledirectory.com.mm/categories/garment-textile-accessories/sewing-machines-accessories.html?q=Sewing%20Machines%20&Accessories=",
        "https://www.textiledirectory.com.mm/categories/garment-textile-accessories/textile-garment-accessories.html?q=Textile%20&Garment_Accessories=",
        "https://www.textiledirectory.com.mm/categories/garment-textile-accessories/textile-garment-machinery.html?q=Textile%20&Garment_Machinery=",
        "https://www.textiledirectory.com.mm/categories/garment-textile-accessories/thread.html?q=Thread",
        "https://www.textiledirectory.com.mm/categories/garment-textile-accessories/yarn.html?q=Yarn",
        "https://www.textiledirectory.com.mm/categories/garment-textile-accessories/zippers.html?q=Zippers",
        "https://www.textiledirectory.com.mm/categories/manufacturers/garment-factories.html?q=Garment%20Factories",
        "https://www.textiledirectory.com.mm/categories/manufacturers/longyi.html?q=Longyi",
        "https://www.textiledirectory.com.mm/categories/manufacturers/thingan.html?q=Thingan",
        "https://www.textiledirectory.com.mm/categories/manufacturers/weaving-mills.html?q=Weaving%20Mills",
        "https://www.textiledirectory.com.mm/categories/shipping/boxes-cartons.html?q=Boxes%20&Cartons=",
        "https://www.textiledirectory.com.mm/categories/shipping/custom-clearing-agents.html?q=Custom%20Clearing%20Agents",
        "https://www.textiledirectory.com.mm/categories/shipping/freight-forwarder.html?q=Freight%20Forwarder",
        "https://www.textiledirectory.com.mm/categories/shipping/packing-equipment.html?q=Packing%20Equipment",
        "https://www.textiledirectory.com.mm/categories/support-services/boiler-steam-system.html?q=Boiler%20&Steam_System=",
        "https://www.textiledirectory.com.mm/categories/support-services/dyeing-and-finishing-machinery.html?q=Dyeing%20and%20Finishing%20Machinery",
        "https://www.textiledirectory.com.mm/categories/support-services/fashion-designer.html?q=Fashion%20Designer",
        "https://www.textiledirectory.com.mm/categories/support-services/tailors.html?q=Tailors",
        "https://www.textiledirectory.com.mm/categories/training/fashion-design-training.html?q=Fashion%20Design%20Training",
        "https://www.textiledirectory.com.mm/categories/training/sewing-classes.html?q=Sewing%20Classes",
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

        # Variables with all xpaths
        name = "//meta[@property='og:title']/@content"
        image_url = "//div[@class='item active']/a/@href"
        address = "//dd[1]/text() | //div[@class='address'][2]/p/text()"
        township = "//dd[2]/text()"
        phone_number = "//dd[3]//a/text() | //div[@class='address'][3]//a/text()"
        website_url = "//label[contains(text(), 'Website')]/../p/a/text() | //dl[@class='dl-horizontal']//a[@rel='nofollow']/text()"
        social_media_links = "//a[@title='Facebook']/@href"
        category = "//div[@class='address'][1]/p/text()"
        company_profile = (
            "//div[@class='col-lg-12 col-md-12 col-xs-12 col-sm-12']/p/text()"
        )
        # Brands_and_services is more complicated, scroll down to find their xpaths.
        # Business_categories is more complicated, scroll down to find their xpaths.
        # Email below

        # Adds company profile url
        l.add_value("url", response.url)

        # Adds company name
        l.add_xpath("name", name, MapCompose(str.strip))

        # Adds image url
        if l.get_xpath(image_url):
            l.add_xpath("image_url", image_url, MapCompose(str.strip))

        # Adds address
        l.add_xpath("address", address, MapCompose(str.strip))

        # Adds township
        if l.get_xpath(township):
            l.add_xpath("township", township, MapCompose(str.strip))

        # Adds phone number
        l.add_xpath("phone_number", phone_number, Join(""), MapCompose(str.strip))

        # Adds email
        if l.get_xpath("//dd[4]//span/@data-cfemail"):
            email = l.get_xpath("//dd[4]//span/@data-cfemail")[0]
            l.add_value("email", decode_email(email))

        # Adds website url
        if l.get_xpath(website_url):
            l.add_xpath("website_url", website_url, MapCompose(str.strip))

        # Adds social media links
        if l.get_xpath(social_media_links):
            l.add_xpath("social_media_links", social_media_links, MapCompose(str.strip))

        # First field
        if l.get_xpath("//h2[@class='h-businessCat'][1]/text()"):
            first_field_name = l.get_xpath("//h2[@class='h-businessCat'][1]/text()")[0]
            first_field_text = "//div[@class='business-category'][1]/ul/li/text()"

            if first_field_name == "Business Categories":
                l.add_xpath(
                    "business_categories",
                    first_field_text,
                    Join(" "),
                    MapCompose(str.strip),
                )
            elif first_field_name == "Brands / Services":
                l.add_xpath(
                    "brands_and_services",
                    first_field_text,
                    Join(" "),
                    MapCompose(str.strip),
                )

        # Second field
        if l.get_xpath("//h2[@class='h-businessCat'][2]/text()"):
            second_field_name = l.get_xpath("//h2[@class='h-businessCat'][2]/text()")[0]
            second_field_text = "//div[@class='business-category'][2]/ul/li/text()"

            if second_field_name == "Business Categories":
                l.add_xpath(
                    "business_categories",
                    second_field_text,
                    Join(" "),
                    MapCompose(str.strip),
                )
            elif second_field_name == "Brands / Services":
                l.add_xpath(
                    "brands_and_services",
                    second_field_text,
                    Join(" "),
                    MapCompose(str.strip),
                )

        # Adds category
        if l.get_xpath(category):
            l.add_xpath("category", category, MapCompose(str.strip))

        # Adds company profile
        if l.get_xpath(company_profile):
            l.add_xpath("company_profile", company_profile, MapCompose(str.strip))

        return l.load_item()
