# -*- coding: utf-8 -*-

# Scrapy settings for spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider (+http://www.yourdomain.com)'
USER_AGENT= 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
#重定向关闭 自己加的
REDIRECT_ENABLED = False
#DEPTH_LIMIT=100
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#   'Accept-Encoding': 'gzip,deflate,sdch',
#   'Accept-Language': 'zh-CN,zh;q=0.8',
#   'Connection':'keep-alive',
#   'Cookie': 'global_cookie=6noxd9kubsghuk29or6dhlrmd1oistwjlfh; searchLabelN=1_1476063513_3574%5B%3A%7C%40%7C%3A%5De57471026e652b690e935c4ffda2ec73; searchConN=1_1476063513_3893%5B%3A%7C%40%7C%3A%5D3a282611e2da3aa8568b10ffa50a08dd; passport=username=&password=&isvalid=1&validation=; factoryDetail_=%7C1010528103%u03B6%u671D%u9633%u673A%u573A%u7B2C%u4E8C%u9AD8%u901F%u5E93%u623F%u03B6%7C; _jzqx=1.1476930975.1477299693.5.jzqsr=newhouse%2Efang%2Ecom|jzqct=/house/s/b92/.jzqsr=newhouse%2Efang%2Ecom|jzqct=/house/s/b81-b932/; _jzqckmp=1; new_search_uid=026ffd5bdb7a589d8b42a60ae78d00e2; newhouse_chat_guid=81463E36-E4B8-D3AA-98D8-4C5EAA119155; recentViewlpNew_newhouse=1_1476823449_2095%5B%3A%7C%40%7C%3A%5Dd7655c021ffcf9b5af520569b9c8bed8; vh_newhouse=1_1473313970_10224%5B%3A%7C%40%7C%3A%5D22e0119302c5e4c23ecc76bfa110e182; newhouse_user_guid=10A530B6-4904-98D2-53E0-EB728DF89FF8; _jzqa=1.3805844646053927000.1476930975.1477450089.1477460068.9; _jzqc=1; token=; Captcha=6B47766861683666547436552F76466775444845486251334D534833334B33344A73375473483376467243753155304C595A5A5743593264546B30556F416A57574C7568516A78585251733D; showAdquanguo=1; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; sf_source=; s=; indexAdvLunbo=lb_ad6%2C0; unique_cookie=78706F4D6D522F5741417A73317074473050532F*6; city=www; __utma=147393320.2038825322.1473313040.1477460067.1477466384.53; __utmb=147393320.9.10.1477466384; __utmc=147393320; __utmz=147393320.1477466384.53.28.utmcsr=newhouse.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/house/s/'
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'spider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'spider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'spider.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
