# -*- coding: utf-8 -*-
import scrapy
import re
from fangtianxia.items import FangtianxiaItem
from scrapy_redis.spiders import RedisSpider
class FtxSpider(RedisSpider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    #start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "https://www.fang.com/SoufunFamily.htm"
    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s","",province_text)
            if province_text:
                province = province_text
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get() #获取城市名称
                city_url = city_link.xpath(".//@href").get() #获取城市链接
                url_module = city_url.split("//")
                scheme = url_module[0]
                domain = url_module[1]
                if 'bj.' in domain:
                    newhouse_url = "http://newhouse.fang.com/house/s/"
                    esf_url = "http://esf.fang.com"
                else:
                    newhouse_url = scheme + '//' + 'newhouse.' + domain + 'house/s/' #新房链接
                    esf_url = scheme + '//' + 'esf.' + domain
                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,
                                     meta={"info":{province,city}})

                yield scrapy.Request(url=esf_url,callback=self.parse_esf,
                                     meta={"info": {province, city}})



    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get()

            # 过滤穿插的广告li
            if name is None:
                continue
            else:
                name = name.strip()

            # 从html中解析数据
            house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            house_type_list = list(map(lambda x:re.sub(r"\s","",x),house_type_list))
            rooms = list(filter(lambda x:x.endswith("居"),house_type_list))
            area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r"\s|－|/","",area)
            address = li.xpath(".//div[@class='address']/a/@title").get()
            district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            district = re.search(r".*\[(.+)\].*",district_text)
            if district is None:
                pass
            else:
                district = district.group(1)
            sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s|广告","",price)
            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            # origin_url = re.sub(r"\s|/","",origin_url)

            # 构造item
            item = FangtianxiaItem(name=name,rooms=rooms,area=area,province=province,city=city,address=address,
                                   district=district,origin_url=origin_url,price=price,sale=sale)
            yield item

            next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").getall()

            if next_url:
                if len(next_url) == 1:
                    url = next_url[0]
                else:
                    url = next_url[1]
                yield scrapy.Request(url=response.urljoin(url),callback=self.parse_newhouse,meta={"info":(province,city)})

    def parse_esf(self, requset):
        pass