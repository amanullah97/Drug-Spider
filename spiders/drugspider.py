import scrapy
import re
from datetime import datetime


class DrugSpider(scrapy.Spider):
    name = 'drugstore'
    start_urls = ["https://www.drugs.com/"]

    def parse(self, response):
        drug_links = response.css("#tab-section-1 nav li a::attr(href)").getall()
        links = drug_links[:-1]
        condition_links = response.css("#tab-section-2 nav li a::attr(href)").getall()
        yield from response.follow_all(links + condition_links, callback=self.parse_drugs)

    def parse_drugs(self, response):
        drug_urls = response.css("nav.ddc-paging.paging-list-wrap.ddc-mgb-2 li a::attr(href)").getall()
        check_url = response.url
        for drug in drug_urls:
            yield response.follow(drug, callback=self.parse_drugs_names, meta={'check_url': check_url})

    def parse_drugs_names(self, response):
        check_url = response.meta.get('check_url')
        drugs_names = response.css("ul.ddc-list-column-2 li a::attr(href)").getall()
        for link in drugs_names:
            yield response.follow(link, callback=self.parse_details, meta={'check_url': check_url})

    def parse_details(self, response):
        check_url = response.meta.get('check_url')
        item_type = "Condition" if "/condition" in check_url else "Drug"
        url = response.url
        medically_reviewed = response.css("div.contentBox span ::text").getall()
        drug_review = self.extract_review(medically_reviewed)
        drug_review = False if drug_review is None else True
        date = response.css(".ddc-reviewed-by span::text").re_first("on(.*\.)")
        if date is not None:
            date = self.extract_date(date)

        reviews = response.css("div.ddc-rating-summary a::text").re_first(r"(\d+)")
        if reviews is not None:
            reviews = int(reviews)

        ratings = response.css("div.ddc-rating-summary b::text").get()
        if ratings is not None:
            ratings = float(ratings)

        yield {
            'url': url,
            'name': response.css("div.contentBox h1::text").get(),
            'genericName': response.css("b:contains('Generic name:') + a::text").get(),
            'medicallyReviewed': drug_review,
            'lastUpdate': date,
            'drugClass': response.css("b:contains('Drug class:') + a::text").get(),
            'ratings': ratings,
            'reviews': reviews,
            'itemType': item_type

        }

    def extract_date(self, date):
        pattern = "[A-z]{4}"
        match = re.search(pattern, date)
        if match:
            dt = datetime.strptime(date.strip(), "%B %d, %Y.")
            final_date = dt.strftime("%Y-%m-%d")
            return final_date

        dt = datetime.strptime(date.strip(), "%b %d, %Y.")
        final_date = dt.strftime("%Y-%m-%d")
        return final_date

    def extract_review(self, review):
        r = ''.join(review)
        pattern = "reviewed\sby\s(.*?)\."
        match = re.findall(pattern, r)
        return match[0] if match else None




