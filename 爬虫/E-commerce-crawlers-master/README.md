## :rocket:电子商务网站爬虫合集
1、[**jd_phone**](https://github.com/Hopetree/E-commerce-crawlers/tree/master/jd_phone)
- 项目简介：京东搜索全平台所有手机参数信息
- 作用：这个不仅仅针对手机，其实可以扩展为京东所有类型的商品的信息爬取
- 主要库：
`selenium`
`lxml`
`requests`
`json`
`re`
- 信息效果：</br>
![](https://github.com/Hopetree/E-commerce-crawlers/blob/master/jd_phone/0001.png)

2、[**天猫品牌搜索**](https://github.com/Hopetree/E-commerce-crawlers/tree/master/%E5%A4%A9%E7%8C%AB%E5%93%81%E7%89%8C%E6%90%9C%E7%B4%A2)
- 项目简介：获取天猫品牌搜索中某个关键词的全部店铺信息（所有店铺名称、链接、相关商品数量、总商品数量等）
- 作用：可以很直观的得知某个关键词（主要是品牌）所包含的商品信息，包括天猫店铺和店铺中相关商品数量等。这个爬虫获取的数据，对于想要在天猫开店的商家有重大参考意义。
- 主要库：
`selenium`
- 信息效果：</br>
![](https://github.com/Hopetree/E-commerce-crawlers/blob/master/%E5%A4%A9%E7%8C%AB%E5%93%81%E7%89%8C%E6%90%9C%E7%B4%A2/001.png)

3、[**天猫商品评价标签**](https://github.com/Hopetree/E-commerce-crawlers/tree/master/%E5%A4%A9%E7%8C%AB%E5%95%86%E5%93%81%E8%AF%84%E4%BB%B7%E6%A0%87%E7%AD%BE)
- 项目简介：批量获取天猫单个商品的评价标签关键词
- 作用：可以从商品标签词中统计出每个商品在买家评论中的优点和缺点，可以帮助商家快速的整改评论不好的商品，提升商品DSR。
- 主要库：
`requests`
- 信息效果：</br>
![](https://github.com/Hopetree/E-commerce-crawlers/blob/master/%E5%A4%A9%E7%8C%AB%E5%95%86%E5%93%81%E8%AF%84%E4%BB%B7%E6%A0%87%E7%AD%BE/0001.png)

4、[**模拟登陆淘宝**](https://github.com/Hopetree/E-commerce-crawlers/tree/master/login_taobao)
- 项目简介：使用账号密码模拟登陆淘宝
- 作用：登陆了淘宝就可以进一步获取更多信息
- 主要库：
`selenium`

5、[**天猫店铺全店商品（手机端）信息提取爬虫**](https://github.com/Hopetree/E-commerce-crawlers/blob/master/tm-products-m/tm-mobie.py)
- 项目简介：爬取指定天猫店铺手机端全店商品信息，包括商品ID、价格、月销量、总销量、标题、链接、主图链接等
- 不过经过对比页面，发现销售信息有点不符合页面展示的数据，这个具体原由不知道是天猫特意给的错误信息来防止爬虫还是本身的信息是有缓存延迟展现的
- 主要库：
`requests`
`json`
`csv`
- 信息效果：</br>
![](https://github.com/Hopetree/E-commerce-crawlers/blob/master/tm-products-m/tm_m.png)

6、[**天猫店铺全店商品scrapy版**](https://github.com/Hopetree/E-commerce-crawlers/tree/master/ECspiers)
- 项目简介：爬取手机天猫某个店铺全部商品的基本信息，scrapy 爬虫
- 主要库：
`scrapy`


