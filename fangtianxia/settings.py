# -*- coding: utf-8 -*-

# Scrapy settings for fangtianxia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fangtianxia'

SPIDER_MODULES = ['fangtianxia.spiders']
NEWSPIDER_MODULE = 'fangtianxia.spiders'

# Obey robots.txt rules 机器人协议
ROBOTSTXT_OBEY = False

# 下载延迟 默认为0
DOWNLOAD_DELAY = 0

# 应用随机请求头中间件
SPIDER_MIDDLEWARES = {
   'fangtianxia.middlewares.FangtianxiaAgentMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'fangtianxia.middlewares.FangtianxiaDownloaderMiddleware': 543,
#}


ITEM_PIPELINES = {
   'fangtianxia.pipelines.FangtianxiaPipeline': 300,
}


# 使用scrapy-redis里的去重组件，不使用scrapy默认的去重方式
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 使用scrapy-redis里的调度器组件，不使用默认的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 允许暂停，redis请求记录不丢失
SCHEDULER_PERSIST = True

# 默认的scrapy-redis请求队列形式（按优先级）
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# 指定数据库的主机IP
REDIS_HOST = "192.168.147.1"
# 指定数据库的端口号
REDIS_PORT = 6379


# MONGODB 主机名
MONGODB_HOST = "192.168.147.1"
# MONGODB 端口号
MONGODB_PORT = 27017
# 数据库名称
MONGODB_DBNAME = "fangtianxia"
# 存放数据的表名称
MONGODB_SHEETNAME = "newhouse"