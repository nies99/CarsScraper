#Scrapy Python
#Finished @ Friday, November 4th 2016 13.30 WIB
#Created by : Hendi Santika
#Waslap / Telegram : +6281321411881
#Skype : hendi.santika 

import MySQLdb
import re

import scrapy
from tld import get_tld


class Tes1(scrapy.Spider):
    name = "carmudi"
    start_urls = [
        'http://www.carmudi.co.id/cars/',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "scrapyDB")
        self.stmt = "insert into cars(url, title, price, posted, city, province, contact_person, description, " \
                    "source_site, year, transmission, brand, model, type, ownership, nego, uploaded_by, phone, seen) " \
                    "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        urls = response.xpath('//section[contains(@class, "catalog-listing")]//h5[contains(@class, "item-title")]/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request

        # process next page
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span/a/@href').extract_first()
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div[2]/span[16]/a/@href').extract_first() # YANG INI UNTUK NGETES DOANG
        current_page = int(response.xpath('//ul[contains(@class,"pagination")]/li[@class="current"]/a/text()').extract_first())
        last_page = int(response.xpath('//ul[contains(@class,"pagination")]/li[last()]/a/text()').extract_first())
        next_page_url = '?page=%d' % (current_page+1 if current_page < last_page else None,)
        if next_page_url is None:
            return

        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        c = self.db.cursor()
        title = response.xpath('//div[@class="title-bar"]/span/text()').extract_first().strip()
        price_tmp = response.xpath('//div[contains(@class, "car-value")]/output/text()').extract_first().strip()
        price = re.sub('[Rp. ]', "", price_tmp)
        address = (' '.join(response.xpath('//div[@id="addressBlock"]/address/text()').extract()).strip()).split('\n')[0].strip()
        city = ''
        province = address
        posted = response.xpath('//p[@class="submitted"]/span[1]/text()').extract_first().strip()
        cp = response.xpath('//p[contains(@class, "dealer-name")]//strong/text()').extract_first()
        desc = '\n'.join(response.xpath('//div[contains(@class, "description")]/p/text()').extract())
        ss = get_tld(response.url)
        year = ''
        transmission = response.xpath('//i[contains(@class,"icon-gearshift")]/following-sibling::span/text()').extract_first()
        brand = response.xpath('//ol[@class="breadcrumbs"]/li[3]/a/span/text()').extract_first()
        model = response.xpath('//ol[@class="breadcrumbs"]/li[4]/a/span/text()').extract_first()
        color = ''.join(response.xpath('//div[@id="details"]//li/span[text()="Golongan Warna"]/parent::li/text()').extract()).strip()
        engine_capacity = response.xpath('//i[contains(@class,"icon-engine")]/following-sibling::span/text()').extract_first()
        engine_type = response.xpath('//i[contains(@class,"icon-fuel")]/following-sibling::span/text()').extract_first()
        doors = ''.join(response.xpath('//div[@id="details"]//li/span[text()="Pintu"]/parent::li/text()').extract()).strip()
        radio = ''.join(response.xpath('//span[text()="Radio"]/parent::li/text()').extract()).strip()
        cd_player = ''.join(response.xpath('//span[text()="CD Player"]/parent::li/text()').extract()).strip()
        tipe = ''
        ownership = ''
        gps = ''
        color = response.xpath('//*[@id="details"]/div[2]/div[1]/ul/li[1]/text()').extract_first().strip()
        doors = response.xpath('//*[@id="details"]/div[2]/div[1]/ul/li[2]/text()').extract_first().strip()
        airbags = response.xpath('//*[@id="Interior>"]/div[2]/div[1]/ul/li[1]/text()').extract_first().strip()
        radio = response.xpath('//*[@id="Interior>"]/div[2]/div[2]/ul/li[1]/text()').extract_first().strip()
        cd_player = response.xpath('//*[@id="Interior>"]/div[2]/div[2]/ul/li[2]/text()').extract_first().strip()
        nego = response.xpath('/html/body/aside/div[1]/main/section[2]/section/div[2]/div[1]/div[2]/div[1]/p/text()').extract_first().strip()
        uploaded_by = ''
        phone = response.xpath('//input[@name="seller_phone"]/@value').extract_first()
        seen = ''

        c.execute(
            "insert into jualo_cars(url, title, city, province, description, price, contact_person, source_site, year, brand,  "
            "model, type, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, gps, radio, cd_player,  "
            "posted, nego, uploaded_by, phone) "
            "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (response.url, title, city, province, desc, price, cp, ss, year, brand, model, tipe, ownership,
             engine_capacity, transmission, doors, color, airbags, gps, radio, cd_player, posted, nego,
             uploaded_by, phone))
        # self.db.commit()

        cars = {
            'url'           : response.url,
            'title'         : title,
            'price'         : price,
            'city'          : city,
            'province'      : province,
            'posted'        : posted,
            'cp'            : cp,
            'desc'          : desc,
            'url'           : response.url,
            'source_site'   : ss,    
            'transmission'  : transmission,
            'engine_capacity': engine_capacity,
            'brand'         : brand,
            'model'         : model,    
            'engine_capacity': engine_capacity,
            'engine_type'   : engine_type,
            'color'         : color,
            'doors'         : doors,
            'radio'         : radio,
            'cd_player'     : cd_player,
            'type'          : tipe,   
            'year'          : year,   
            'ownership'     : ownership,
            'color'         : color,
            'doors'         : doors,
            'airbags'       : airbags,
            'gps'           : gps,
            'radio'         : radio,
            'cd_player'     : cd_player,
            'nego'          : nego,    
            'uploaded_by'   : uploaded_by,   
            'phone'         : phone,   
            'seen'          : seen   
            }
        yield cars                 



 

              

