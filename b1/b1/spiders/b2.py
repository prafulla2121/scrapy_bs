# import scrapy
# import re
# import json
# import os
# from fake_useragent import UserAgent

# class BusinessStandardSpider(scrapy.Spider):
#     name = "b2"
#     allowed_domains = ["business-standard.com"]
#     start_urls = ["https://www.business-standard.com/"]

#     ua = UserAgent()
#     article_pattern = re.compile(r"^https://www\.business-standard\.com/.*-\d{12}_1\.html$")
#     blacklist_patterns = ["/web-stories", "/video-gallery", "/cricket", "/entertainment",
#                           "/health", "/companies/result", "/education", "/budget-2025",
#                           "/sports", "/lifestyle","/hindi"]
    
#     visited_urls_file = "visited_urls.json"

#     def __init__(self, *args, **kwargs):
#         super(BusinessStandardSpider, self).__init__(*args, **kwargs)
#         self.visited_urls = self.load_visited_links()

#     def load_visited_links(self):
#         """Load visited URLs from JSON file to avoid duplicates across runs."""
#         if os.path.exists(self.visited_urls_file):
#             try:
#                 with open(self.visited_urls_file, "r", encoding="utf-8") as f:
#                     return set(json.load(f))
#             except json.JSONDecodeError:
#                 return set()
#         return set()

#     def save_visited_links(self):
#         """Save visited URLs persistently."""
#         with open(self.visited_urls_file, "w", encoding="utf-8") as f:
#             json.dump(list(self.visited_urls), f, ensure_ascii=False, indent=4)

#     def start_requests(self):
#         for url in self.start_urls:
#             headers = {"User-Agent": self.ua.random}
#             yield scrapy.Request(url=url, headers=headers, callback=self.parse)

#     def parse(self, response):
#         """Extract article links while avoiding duplicates."""
#         if response.status != 200:
#             self.logger.error(f"Failed to access {response.url} - Status Code: {response.status}")
#             return

#         links = response.css("a::attr(href)").getall()

#         for link in links:
#             full_url = response.urljoin(link)

#             # Skip blacklisted and already visited links
#             if any(pattern in full_url for pattern in self.blacklist_patterns) or full_url in self.visited_urls:
#                 continue

#             # Mark as visited
#             self.visited_urls.add(full_url)

#             # Save visited links persistently
#             self.save_visited_links()

#             if self.article_pattern.match(full_url):
#                 self.logger.info(f"✅ Extracted Article URL: {full_url}")
#                 yield {"url": full_url}  # This will be saved to output.csv
#                 yield scrapy.Request(url=full_url, headers={"User-Agent": self.ua.random}, callback=self.parse_article)
#             else:
#                 yield scrapy.Request(url=full_url, headers={"User-Agent": self.ua.random}, callback=self.parse)

#     def parse_article(self, response):
#         """Scrape article content."""
#         yield {"url": response.url}  # Avoids duplicate article entries
import pandas as pd

# Load CSV files (change filenames as needed)
file1 = "scraped_links.csv"
file2 = "new.csv"
file3 = "output.csv"

# Read CSV files and extract URLs
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)

# Ensure all dataframes have a 'url' column
if 'url' not in df1.columns or 'url' not in df2.columns or 'url' not in df3.columns:
    raise ValueError("One or more CSV files do not have a 'url' column")

# Combine all dataframes and remove duplicates
merged_df = pd.concat([df1, df2, df3], ignore_index=True).drop_duplicates(subset="url")

# Save the unique URLs to a new CSV file
merged_df.to_csv("merged_unique_urls.csv", index=False)

print(f"✅ Merged {file1}, {file2}, and {file3} into 'merged_unique_urls.csv' with no duplicates.")
