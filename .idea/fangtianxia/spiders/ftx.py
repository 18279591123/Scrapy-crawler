# -*- coding: utf-8 -*-
import scrapy
import re
from fangtianxia.util import PriorityUrl
from fangtianxia.items import *
from scrapy_redis.spiders import RedisSpider
class FtxSpider(RedisSpider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    url = "https://newhouse.fang.com/house/s/"
    #start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fang"
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
                list = domain.split(".")
                domain = list[0]
                if 'bj' in domain:
                    newhouse_url = "http://newhouse.fang.com/house/s/"
                else:
                    newhouse_url = scheme + '//' +domain+ '.newhouse.fang.com/house/s/' #新房链接 newhouse_url = prefix + 'newhouse.fang' + domain + 'house/s/'
                    print(newhouse_url)
                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,
                                     meta={"province":province,"city":city},priority=PriorityUrl(newhouse_url,"https://newhouse.fang.com/house/s/"))





    def parse_newhouse(self,response):
        province = response.meta.get('province')
        city = response.meta.get('city')
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
                yield scrapy.Request(url=response.urljoin(url),callback=self.parse_newhouse,
                                     meta={"province":province,"city":city},priority=PriorityUrl(response.urljoin(url),"https://newhouse.fang.com/house/s/")) #meta={"info":(province,city)}

    def parse_esf(self,response):
            province, city = response.meta.get('info')
            dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
            for dl in dls:
                item = ESFHouseItem(province=province, city=city)
                name = dl.xpath(".//span[@class='tit_shop']/text()").get()
                if name:
                    infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
                    infos = list(map(lambda  x: re.sub(r"\s", "", x),  infos))
                    for  info  in  infos:
                         if  "厅"  in  info:
                                    item["rooms"] = info
                         elif  '层'  in  info:
                            item["floor"] = info
                         elif '向'  in  info:
                            item['toward'] = info
                         elif  '㎡'  in  info:
                            item['area'] = info
                         elif  '年建'  in  info:
                            item['year'] = re.sub("年建", "", info)
                    item['address'] = dl.xpath(".//p[@class='add_shop']/span/text()").get()
                      #  总价
                    item['price'] = "".join(dl.xpath(".//span[@class='red']//text()").getall())
                      #  单价
                    item['unit'] = dl.xpath(".//dd[@class='price_right']/span[2]/text()").get()
                    item['name'] = name
                    detail = dl.xpath(".//h4[@class='clearfix']/a/@href").get()
                    item['origin_url'] = response.urljoin(detail)
            yield item