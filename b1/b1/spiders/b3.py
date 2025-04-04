import scrapy
import re
import json
import os
from fake_useragent import UserAgent

class BusinessStandardSpider(scrapy.Spider):
    name = "b3"
    allowed_domains = ["business-standard.com"]
    start_urls = ["https://www.business-standard.com/"]

    ua = UserAgent()
    article_pattern = re.compile(r"^https://www\.business-standard\.com/.*-\d{12}_1\.html$")
    blacklist_patterns = ["/web-stories", "/video-gallery", "/cricket", "/entertainment",
                          "/health", "/companies/result", "/education", "/budget-2025",
                          "/sports", "/lifestyle","/hindi"]
    
    visited_urls_file = "visited_urls.json"

    def __init__(self, *args, **kwargs):
        super(BusinessStandardSpider, self).__init__(*args, **kwargs)
        self.visited_urls = self.load_visited_links()

    def load_visited_links(self):
        """Load visited URLs from JSON file to avoid duplicates across runs."""
        if os.path.exists(self.visited_urls_file):
            try:
                with open(self.visited_urls_file, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except json.JSONDecodeError:
                return set()
        return set()

    def save_visited_links(self):
        """Save visited URLs persistently."""
        with open(self.visited_urls_file, "w", encoding="utf-8") as f:
            json.dump(list(self.visited_urls), f, ensure_ascii=False, indent=4)

    def start_requests(self):
        for url in self.start_urls:
            headers = {"User-Agent": self.ua.random}
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        """Extract article links while avoiding duplicates."""
        if response.status != 200:
            self.logger.error(f"Failed to access {response.url} - Status Code: {response.status}")
            return

        links = response.css("a::attr(href)").getall()

        for link in links:
            full_url = response.urljoin(link)

            # Skip blacklisted and already visited links
            if any(pattern in full_url for pattern in self.blacklist_patterns) or full_url in self.visited_urls:
                continue

            # Mark as visited
            self.visited_urls.add(full_url)

            # Save visited links persistently
            self.save_visited_links()

            if self.article_pattern.match(full_url):
                self.logger.info(f"✅ Extracted Article URL: {full_url}")
                yield {"url": full_url}  # This will be saved to output.csv
                yield scrapy.Request(url=full_url, headers={"User-Agent": self.ua.random}, callback=self.parse_article)
            else:
                yield scrapy.Request(url=full_url, headers={"User-Agent": self.ua.random}, callback=self.parse)

    def parse_article(self, response):
        """Scrape article content."""
        yield {"url": response.url}  # Avoids duplicate article entries
