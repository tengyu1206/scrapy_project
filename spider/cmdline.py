import scrapy.cmdline

if __name__ == '__main__':
    #scrapy.cmdline.execute(argv=['scrapy','crawl','dmoz'])
    scrapy.cmdline.execute("scrapy crawl fang_community".split())
    #http://www.rong360.com/wenzhou/fangdai/search?px=1
    #http://www.rong360.com/weifang/fangdai/search?px=1
    #http://www.rong360.com/yantai/fangdai/search?px=1