import scrapy.cmdline

if __name__ == '__main__':
    #scrapy.cmdline.execute(argv=['scrapy','crawl','dmoz'])fang_newhouse
    #scrapy.cmdline.execute("scrapy crawl fang_community".split())
    #scrapy.cmdline.execute("scrapy crawl fang_communityPrice".split())
    scrapy.cmdline.execute("scrapy crawl fang_newhouse".split())
    #scrapy.cmdline.execute("scrapy crawl fang_communityDetail".split())
    #scrapy.cmdline.execute("scrapy crawl fang_newhouseDynamic".split())
    #scrapy.cmdline.execute("scrapy crawl rong360".split())