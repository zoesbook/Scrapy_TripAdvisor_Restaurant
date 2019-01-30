# -*- coding: utf-8 -*-
import scrapy
import string


class ResLasVegasSpider(scrapy.Spider):
    name = 'res_las_vegas'
    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Restaurants-g45963-Las_Vegas_Nevada.html#EATERY_OVERVIEW_BOX']

    def parse(self, response):
        listings = response.xpath('//div[@class="ui_columns is-mobile"]')

        for listing in listings:
            link = listing.xpath('.//a[@class="property_title"]/@href').extract_first()
            text = listing.xpath('.//a[@class="property_title"]/text()').extract_first().strip()

            #yield {"Link" : link,
            #       "Text" : text}

            yield scrapy.Request(response.urljoin(link), callback = self.parse_listing,
                    meta = {'link' : link, 'text' : text})

        next_page_url = response.xpath('//a[@class = "nav next rndBtn ui_button primary taLnk"]/@href').extract_first()

        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback = self.parse)


    def parse_listing(self, response):
        link = response.meta['link']
        text = response.meta['text']

        rating =  response.xpath('//*[@class = "restaurants-detail-overview-cards-RatingsOverviewCard__primaryRatingRow--Ct2Oc"]/span[1]/text()').extract_first()
        review_len = response.xpath('//*[@class = "restaurants-detail-overview-cards-RatingsOverviewCard__primaryRatingRow--Ct2Oc"]/a/text()').extract_first()
        description = response.xpath('//*[@class = "restaurants-detail-overview-cards-SnippetsOverviewCard__heading--3dyNd"]/text()').extract_first()
        location =  response.xpath('//*[@class = "restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--2saB_"]/text()').extract_first()
        price = response.xpath('//*[@class = "header_links"]/a[1]/text()').extract_first()
        brief_des = response.xpath('//div[@class = "header_links"]//text()').extract()
        x = [''.join(c for c in s if c not in string.punctuation) for s in brief_des]
        brief_des = ''.join(x)
        open_now =  response.xpath('//span[@class = "public-location-hours-LocationHours__bold--BYVNh"]//text()').extract_first()

        yield {'text': text, 'rating': rating, 'open': open_now,'review_len': review_len, 'price': price, 'description': description, 'brief_des': brief_des, 'location': location}

