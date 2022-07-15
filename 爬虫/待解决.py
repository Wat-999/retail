import re
from lxml import etree
from parsel import Selector
import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}

def get_goods_id_by_url(response):
    res_html = etree.HTML(response)
    goods_url = res_html.xpath('.//link[@rel="canonical"]/@href')[0].strip()
    goods_id_re = re.compile(r'id=(.*)')
    goods_id = re.findall(goods_id_re, goods_url)[0]
    print('商品id是：'+goods_id) #商品id

def get_goods_title(sel):
    sel_title = sel
    goods_title = sel_title.xpath('//img[@id="J_ImgBooth"]/@alt').extract()[0]
    print('商品标题是：'+goods_title)  #商品标题

def get_goods_mainimages_adress(sel):
    sel_image = sel
    goods_mainimages_adress = sel_image.xpath('//img[@id="J_ImgBooth"]/@src').extract()[0]
    print('商品主图地址是：'+goods_mainimages_adress)  #商品主图地址

def get_goods_price(sel):
    sel_price = sel
    goods_price = sel_price.xpath('//dl[@id="J_PromoPrice"]/div[@class="tm-promo-price"]/span[@class="tm-price"]/text()').extract()
    print('商品价格是：'+goods_price)  #商品价格

def get_goods_shopname(sel):
    sel_shopname = sel
    goods_shopname = sel_shopname.xpath('//div[@id="shopExtra"]/div[@class="slogo"]/a/strong/text()').extract()[0]
    print('店铺地址是：'+goods_shopname)  #店铺名称

def get_goods_shopkeeper(sel):
    sel_shopkeeper = sel
    goods_shopkeeper = sel_shopkeeper.xpath('//div[@class="extend"]/ul/li[@class="shopkeeper"]/div[@class="right"]/a/text()').extract()[0]
    print('掌柜名称是：'+goods_shopkeeper)  #掌柜名称

def get_goods_shopadress(sel):
    sel_shopadress = sel
    goods_shopadress = sel_shopadress.xpath('//div[@class="extend"]/ul/li[@class="locus"]/div[@class="right"]/text()').extract()[0].strip()
    print('店铺地址是：'+goods_shopadress)  #店铺地址

url = "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-21590058420.60.27df50995QpL6i&id=670540008512&rn=409b6ea8f6d3f9c04c285498468dc6e7&abbucket=6"
response = requests.get(url, headers=headers).text
sel = Selector(text=response)
get_goods_id_by_url(response)
get_goods_title(sel)
get_goods_mainimages_adress(sel)
#get_goods_price(sel) #天猫对商品价格加密了，简单地爬虫无法爬取
get_goods_shopname(sel)
get_goods_shopkeeper(sel)
get_goods_shopadress(sel)
