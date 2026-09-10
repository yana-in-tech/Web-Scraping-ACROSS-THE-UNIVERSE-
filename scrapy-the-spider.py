import scrapy


class ProductSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/products"]

    def parse(self, response):
        for product in response.css("article.product-card"):
            yield {
                "name": product.css("h2::text").get(),
                "price": product.css(".price::text").get(),
                "url": response.urljoin(
                    product.css("a::attr(href)").get()
                ),
            }

        next_page = response.css("a.next::attr(href)").get()

        if next_page:
            yield response.follow(next_page, callback=self.pa
                                  rse)
