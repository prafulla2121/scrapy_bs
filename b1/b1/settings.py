BOT_NAME = 'b1'
SPIDER_MODULES = ['b1.spiders']
NEWSPIDER_MODULE = 'b1.spiders'

ROBOTSTXT_OBEY = False

# Control speed and avoid getting blocked
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
CONCURRENT_REQUESTS: 8# Only send one request at a time
COOKIES_ENABLED: False  # Disable cookies (sometimes helps avoid 403)
AUTOTHROTTLE_ENABLED: True  # Enable auto-throttle
AUTOTHROTTLE_START_DELAY: 1  # Initial delay
AUTOTHROTTLE_MAX_DELAY=3



# # Output directly to JSON file
# FEEDS = {
#     "business_standard_articles.json": {
#         "format": "json",
#         "encoding": "utf-8",
#         "overwrite": True  # Overwrites the file if it exists
#     },
# }

# Disable retries to avoid wasting time on bad URLs
RETRY_ENABLED = False

# Timeouts to skip slow pages


# Logging for better tracking
LOG_LEVEL = "INFO"
