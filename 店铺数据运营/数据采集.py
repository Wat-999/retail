import requests
import re
from lxml import etree
import datetime
import json
from urllib import parse
import pandas as pd

# 商品链接
url = 'https://detail.tmall.com/item.htm?id=627845675208'
# 访问参数
headers = {
    'cookie': 'sgcookie=E100/x4Fp7felQg8HPN4v+sbR6VSZGie4CP3SS5jCBFq7wNNrGUhiYwjkyUXJEEKvzXxKNs4JGtXoSx6T0R+q6dvsDi9sJbmNHfI8XXXsdn8frQ=; t=63ffc9d42ef396ca62ae52b08097dd45; uc3=id2=VvaFC40gCTHa&nk2=WvKT2j8C/mV4I+HOIQ==&lg2=WqG3DMC9VAQiUQ==&vt3=F8dCvC3wqW5EraztHQI=; tracknick=924734143\u6B66\u738B; lid=924734143武王; uc4=id4=0@VHAHYjkCJ2ag6stFGY/xADec020=&nk4=0@WDWgZQpk9DAMOq29U9zagkfOW1tQeeEH; lgc=924734143\u6B66\u738B; enc=TB2uKMnnenNWyn0mv79Lb9cVLZ6JSjJ8Bx1KKYxL6zGEE/X3TWSj+9G8F+iBaYcN9iPhIFvVe0xukq+cZF3aGA==; _tb_token_=e93bebeee6607; cookie2=137e8de85caa22e4d98a93c74c087e38; cna=uJIrG8pwBV0CAXjsEqThSJXI; xlly_s=1; _m_h5_tk=9a332970253911f494ec1b615456309b_1657036444845; _m_h5_tk_enc=d15748a334552e1638c52ce5904fec42; pnm_cku822=098#E1hvyvvUvbZvUpCkvvvvvjiWRLSvAj18RscZzjrCPmPhAjDvP2Sp6j3bRLcOsjlbRuOCvvpvvhHhRvhvCvvvphvRvpvhMMGvvv9CvhQmsqKqj76wd3wgnZ43Ib8rV4tiBXxrV4TJ+3+FafmAdBAKNpKYiLUpVCODN+Cl5d8reC61D70OdigXalKxfXKK5u6aWXxreuTJ+3+dKvhv8vvvpVwvvvvvvvCHzvvv9bvvvh7rvvmC4QvvB46vvUhlvvCHzvvv9B0IvpvUvvCCQ2+KTueUvpvjvpC2pWLvevvCvvOvChCvvvv=; tfstk=cHFVBsDfpfq56meDTbhNlvErydgAZWDIQMusnM7CAv59o4HcihKtrFxgL8Tyjxf..; l=eBjGrVsVLZoosPrtXOfwourza77OSIRAguPzaNbMiOCPOWCH5zeGW6AJWHTMC3GVh6VJR3rVZW9zBeYBcoAMhrD1a6Fy_Ckmn; isg=BIiIYQNFfm9C5ZLtTZv_m6v-WfCaMew70XDqekI51IP2HSiH6kG8yx6flfVtLaQT',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    'referer': 'https://detail.tmall.com/item.htm?id=627845675208'
}  #头的问题需要解决？？？？？
#查看cookie值,打开浏览器，进入调试窗口（F12键），然后在网页栏刷新页面，切换到到控制台界面，在Network -> Doc -> Name -> Headers，即可


# 获取HTML数据
response = requests.get(url, headers=headers)
html = response.text

selector = etree.HTML(html)

# 读取商品标题
title = selector.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[1]/h1')
商品标题 = re.compile(u"[^\u4e00-\u9fa5]+").sub('', str(title[0]))
#re.compile()函数用于编译正则表达式，返回一个对象，可以把常用的正则表达式编译成正则表达对象，方便后续调用及提高效率
#"\u4e00-\u9fa5"中文字符的正则表达式，^表示匹配输入字行首。如果设置了RegExp对象的Multiline属性，^也匹配“\n”或“\r”之后的位置。
#"+"匹配前面的子表达式一次或多次(大于等于1次）。例如，“zo+”能匹配“zo”以及“zoo”，但不能匹配“z”。+等价于{1,}。


# 读取商家昵称
shop = selector.xpath('//*[@id="shopExtra"]/div[1]/a/strong/text()')
商家昵称 = shop[0]
# 获取商品ID
params = parse.parse_qs(parse.urlparse(url).query)
商品ID = params['id'][0]
# 获取当前日期
日期 = datetime.datetime.now().strftime('%Y-%m-%d')
# 获取sku名称
listsku = {'id':'名称'}
allsku = selector.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/*')
for i in range(1,len(allsku)+1):
    path1 = '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li['+ str(i) +']/@data-value'
    path2 = '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li['+ str(i) +']/@title'
    id = selector.xpath(path1)
    skuname = selector.xpath(path2)
    listsku[str(id[0])] = str(skuname[0])
# 获取sku价格
text = selector.xpath('//*[@id="J_DetailMeta"]/div[1]/script[3]/text()')
listmoney = {'skuid':'价格'}
for match in re.finditer('{"priceCent":(.*?),"price":"(.*?)","stock":(.*?),"skuId":"(.*?)"}',text[0]):
    moneyinfo = json.loads(match.group())
    skuid = moneyinfo['skuId']
    money = moneyinfo['price']
    listmoney[skuid] = money
# 获取skuID,名称,价格,输入到DataFrame中
skuData = pd.DataFrame(columns = ['日期', '商家昵称', '商品ID', 'SKUID', 'SKU名称', 'SKU价格'])
for match in re.finditer('{"names":"(.*?)","pvs":"(.*?)","skuId":"(.*?)"}',text[0]):
    skuinfo = json.loads(match.group())
    SKUID = skuinfo['skuId']
    SKU名称 = '尺码:'+ skuinfo['names'].split(' ')[1] + '颜色分类:'+ listsku[skuinfo['pvs'][0:13]]
    SKU价格 = listmoney[SKUID]
    # 写入到DataFrame
    data = {'日期': 日期, '商家昵称': 商家昵称, '商品ID': 商品ID, 'SKUID': SKUID, 'SKU名称': SKU名称, 'SKU价格': SKU价格}
    skuData = skuData.append(data,ignore_index=True)

# 写入到Excel文件
skuData.to_excel('单品价格.xls')
print('完成')