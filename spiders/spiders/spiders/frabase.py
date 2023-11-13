import scrapy
from pathlib import Path


class FrabaseSpider(scrapy.Spider):
    name = "frabase"
    allowed_domains = ["rnafrabase.cs.put.poznan.pl"]
    start_urls = [
        r"http://rnafrabase.cs.put.poznan.pl/index.php?act=secondary%20structures"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_main)

    def parse_main(self, response):
        pdb_ids = response.xpath(
            "//div[@id='fracontent']//form/table//tr/td/a/text()"
        ).getall()[::3]
        details_links = response.xpath(
            "//div[@id='fracontent']//form/table//tr/td/a/@href"
        ).getall()[2::3]

        Path("../data/frabase/pdb_ids.txt").write_text(
            "\n".join(pdb_ids), encoding="utf-8"
        )

        for details_link in details_links:
            yield response.follow(
                url=details_link,
                callback=self.parse_details,
            )

    def parse_details(self, response):
        pdb_id = response.xpath("//a[@class='a2']/text()").get()
        structures = response.xpath("//td[@class='details']/text()").getall()
        structures = "\n".join(structures)
        Path(f"../data/frabase/2D/{pdb_id}.txt").write_text(structures)
