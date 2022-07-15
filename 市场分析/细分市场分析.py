#思路
#1根据杀虫剂的类别对数据进行汇总统计
#2根据价格分组，计算一个商品分配对销售额，计算方式为：预估销售额/商品数，其中商品数是商品ID对计数汇总项。商品分配的销售额越大，说明该细分市场相对容易做。
#3根据商品特征分组
#4分析消费者评价，对消费者评价进行分词，并绘制词云图，以此了解消费者对需求

#类别对分布分析
import matplotlib.pyplot as plt
import pandas as pd

d1 = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/灭鼠杀虫剂细分市场/螨.xlsx')
d2 = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/灭鼠杀虫剂细分市场/灭鼠.xlsx')
d3 = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/灭鼠杀虫剂细分市场/杀虫.xlsx')
d4 = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/灭鼠杀虫剂细分市场/虱子.xlsx')
d5 = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/灭鼠杀虫剂细分市场/蟑螂.xlsx')

#将各类别的属性和销售额索引出来
a1 = d1.loc[:, ['类别', '预估销售额']]
a2 = d2.loc[:, ['类别', '预估销售额']]
a3 = d3.loc[:, ['类别', '预估销售额']]
a4 = d4.loc[:, ['类别', '预估销售额']]
a5 = d5.loc[:, ['类别', '预估销售额']]

#合并数据集
data = pd.concat([a1, a2, a3, a4, a5])

#按照类别进行分组求和汇总
data2 = data.groupby('类别').sum()

#计算每一个类别占总体的份额比例，保留两位小数
# data2['份额占比'] = data2/data2.sum().values
# data2['份额占比'] = data2['份额占比'].apply(lambda x: format(x, '.2%'))  #装换为百分比格式
data2['份额占比'] = round(data2/data2.sum().values*100, 2)  #也可以不加百分比
print(data2)

#绘制条形图：类别的绝对份额可使用条形图展示，类别的相对份额可使用月饼图展示

#设置参数，以确保图形正确显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

#将产品分类设置为条形图的y坐标轴，销售额设置为条形图的X坐标轴
cate = list(data2.index)
value = data2.iloc[:, 0]

#设置画布大小
pl = plt.figure(figsize=(10, 6))
#绘制条形图
plt.barh(cate, value)
#设置图标题，x轴标题，y轴标题
plt.title('"灭鼠灭虫"市场各类产品类别销售分布', pad=20)
plt.xlabel('销售额')
plt.ylabel('类别')
plt.show()

#绘制饼图
#设置画布
pl = plt.figure(figsize=(8, 6))

#将类别设置成标签，将份额占比设置为大小
labels = list(data2.index)
sizes = data2['份额占比'].values.tolist()
#绘制饼图
plt.pie(sizes, labels=labels, autopct='%.1f%%', shadow=False, startangle=180)
#设置图标题
plt.title('各产品类别的相对份额占比')
plt.axis('equal')
plt.show()


#识别潜力细分市场
#本节以灭鼠产品市场为例，可以切分多个细分市场，如根据价格区间切割

#1准备数据：根据业务理解删除无关字段
d2.drop(['时间', '页码', '排名', '链接', '主图链接', '主图视频链接', '宝贝标题', '下架时间', '旺旺'], axis=1, inplace=True)
# 遍历每一个字段，删除仅包含一种信息的字段
for i in d2.columns:
    if len(d2[i].value_counts()) <= 1:
        del d2[i]
# 缺失值大于90%的字段删除
for i in d2.columns:
    if d2[i].isnull().sum() > d2.shape[0]*0.9:  #isnull()函数用于判断缺失值、shape[0]表示输出矩阵的行数、shape[1]表示输出矩阵的列数、np.shape(k)输出矩阵的行和列数
        del d2[i]
#print(d2.head())

#value_counts()函数可以对Series里面的每个值进行计数并且排序(加参数ascending=True）及计数占比(加参数normalize=True)
#df.isnull().any()会判断哪些列包含缺失值，该列存在缺失值则返回True，反之False
#isnull().sum()就更加直观了，它直接告诉了我们每列缺失值的数量

#根据价格区间细分市场
#价格区间是市场的基础属性，在切割价格区间需要设定步长、步长的大小要看价格区间的范围以及消费者对价格的敏感度
d2.describe()  #描述性统计函数 发现数据集售价字段的范围在0～498元

#定出7个价格区间，前6个价格区间步长为50元
databins = [0, 50, 100, 150, 200, 250, 300, 1000]
datalebels = ['0-50', '51-100', '101-150', '151-200', '201-250', '251-300', '300-1000']
d2['价格区间'] = pd.cut(d2['售价'], bins=databins, labels=datalebels, include_lowest=True)
#离散化分段统计函数：cut()；bins (表示分段数或分类区间，可以是数字，比如说4，就是分成4段，也可以是列表，表示各段的间隔点)
#labels(表示结果标签，一般最好添加，方便阅读和后续统计)
#include_lowest：它包含一个布尔值, 该布尔值用于检查第一个间隔是否应为左包含性。

#接下来计算不同价格区间的销售额(本案例中，销售额的计算使用数据表中的"预估销售额"字段)、销售额占比，销量、销量占比
#删除重复的商品ID
d_id = d2.iloc[list(d2.宝贝ID.drop_duplicates().index), :]  #drop_duplicates()为去重函数，默认保留重复项最后一个
#drop_duplicates().index 取重复项值的索引

#分组汇总
bins1 = d_id.groupby('价格区间').sum()

bins1['销售额占比'] = round(bins1.预估销售额/bins1.apply(lambda x: x.sum())[3]*100, 2)
#bins1.apply(lambda x: x.sum())[3],其中[3]表示的意思是在数据表bins1用匿名函数对指定列(这里为预估销售额)进行汇总求和，其预估销售额在表的位置刚好是第4列即[3]

#计算销量占比
bins1['销量占比'] = round(bins1['销量（人数）']/bins1.apply(lambda x: x.sum())[1]*100, 2)


#提取bins1中的字段
bins2 = bins1.loc[:, ['预估销售额', '销售额占比', '销量（人数）', '销量占比']]
# print(bins2)

#计算不同价格区间内的商品数
bins3 = d_id.groupby('价格区间').宝贝ID.nunique() #nuinque()是查看该序列(axis=0/1对应着列或行)的不同值的数量。用这个函数可以查看数据有多少个不同值
bins2['商品数'] = bins3
bins2['商品数占比'] = round(bins2['商品数']/bins2.apply(lambda x: x.sum())[4]*100, 2)

#计算一件商品分配到的平均销售额
bins2['一件商品分配到的销售额'] = round(bins2.预估销售额/bins2.商品数, 2)
bins2.sort_values(by='一件商品分配到的销售额', ascending=False, inplace=True) #有时执行排序不成功，添加参数inplace即可表示为立即修改
# print(bins2)
#发现0～50元价格区间的销量相对占比最大，可以进一步分析这个区间，把步长设置10元为一个区间。要注意的是，并不是销量占比越大越好，0～50元价格区间的
#销量占比大的同时，商品数占比也最大，平均一个商品分配到的销售额并不高，因此在选择价格区间时还需要综合考量


#3减少步长继续细分价格区间，
#提取0～50元价格区间的数据，
mark_50 = d_id.copy()
mark_50 = mark_50[d_id.售价 < 50]

#以10元为步长创建子价格区间
databins = [0, 10, 20, 30, 40, 50.1]  #标签比标签边缘小于0.01
datalebels = ['0-10', '11-20', '21-30', '31-40', '41-50']
mark_50['价格区间'] = pd.cut(mark_50['售价'], bins=databins, labels=datalebels, include_lowest=True)


# 由于每一个价格区间都需要剖析分析，此处将上述价格分析流程封装成函数
data = pd.DataFrame()
def price_mark(data):
    # 计算得到价格区间的销售额、销售额占比、销量、销量占比。
    bins_1 = data.groupby('价格区间').sum()
    bins_1['销售额占比'] = round(bins_1.预估销售额 / bins_1.apply(lambda x: x.sum())[3] * 100, 2)
    bins_1['销量占比'] = round(bins_1['销量（人数）'] / bins_1.apply(lambda x: x.sum())[1] * 100, 2)
    bins_2 = bins_1.loc[:, ['预估销售额', '销售额占比', '销量（人数）', '销量占比']]
    # 计算得到宝贝数，宝贝数占比、宝贝分配
    # 分组非重复计数(不同价格区间内的宝贝数)
    bins_3 = data.groupby('价格区间').宝贝ID.nunique()
    bins_2['商品数'] = bins_3
    bins_2['商品数占比'] = round(bins_2['商品数'] / bins_2.apply(lambda x: x.sum())[4] * 100, 2)
    bins_2['一个商品分配的销售额'] = round(bins_2.预估销售额 / bins_2.商品数, 2)
    res = bins_2.sort_values(by='一个商品分配的销售额', ascending=False)
    return res

#print(price_mark(mark_50))
#11～20元子价格区间在0～50元价格区间中是最优选择，销售额占比、销量量占比都市最大的，一件商品分配的销售额也是最大，商品数占比32%，排名第二
#相比21～30元子价格区间的数据已经非常优秀了

#同理可以深度剖析101～150元价格区间
mark_2 = d_id.copy()
mark_2 = mark_2[(d_id.售价 > 100) & (d_id.售价 < 150)]
data_bins = range(100, 151, 10)
data_lebels = ['100-110', '111-120', '121-130', '131-140', '141-150']
mark_2['价格区间'] = pd.cut(mark_2['售价'], bins=data_bins, labels=data_lebels, include_lowest=True)
print(price_mark(mark_2))   #调用函数

#潜力细分市场需求分析
#市场需求分析是指了解市场需要的产品类型、需要数量以及对产品发展的要求，包括产品对性状、规格、用途、产品在市场上的需求量、实际销售量，以及与同类产品规格、
#性能等方面的分析比较等。
#通过分析不难发现，在101～150元区间中，131～140元子价格区间竞争度低，是不错的切入价格段。于是，我们对该价格区间的商品需求进一步分析挖掘

#准备好数据
mark_select = d_id[(d_id.售价 > 130) & (d_id.售价 < 140)]  #d_id是过滤掉商品重复ID的数据集
#mark_select = mark_select.drop(['宝贝ID'], axis=1, )  #删掉宝贝ID字段，用于汇总

#根据店铺类型分组汇总数据
d_shop = mark_select.groupby('店铺类型').sum()

#根据适用对象分组汇总数据
Suitable = mark_select.groupby('适用对象').sum()

#根据品牌分组汇总数据
brand = mark_select.groupby('品牌').sum()

#根据物理形态分组汇总数据
mark_select.groupby('物理形态').sum()

#根据型号分组汇总数据
mark_select.groupby('型号').sum()

#消费者需求分析
#用户表达需求的方式除了谈么的购买行为，还包括评论等文本数据。文本数据中蕴含等信息等价值毋庸置疑。但是文本数据为非结构化数据，树立难度大
#下面先来看一下文本分析大定义：指对文本对表示及其特征项对选取。文本分析是文本挖掘、信息检索的一个基本问题，它把从文本中抽取出的特征词进行量化来表示文本信息。
#文本的语义不可避免地会反映人的特定立场、观点、价值和利益。因此，由文本内容分析，可以推断文本提供者的需求和目的

#接下来就以某款热销商品的评论数据来进行文本分析，探索用户需求
#1准备数据
goods = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/产品评论数据.xlsx')

#2探索数据
goods.head()

#3查看评论中的重复数量
goods.评论.value_counts() #python中counts不单独使用需要加value,count则为单独使用函数

#4文本数据的预处理
#通过对文本数据对探索，我们发现商品对评论中存在这一些杂乱数据

#用户购买后未进行评论时，系统会默认生成"此用户没有填写评论"，而这样对信息无法表述出用户对需求，故予以删除
goods = goods[goods.评论 != '此用户没有填写评论!']  #删除不需要的=索引需要的

#索引需要的数据后，索引并没有发生改变，故重置一下索引
goods.reset_index(inplace=True)
#重置索引后，原有的索引会作为新的列添加到dataframe(数据框)中，故删除该列
del goods['index']
#print(goods)

#list_goods = goods.评论.values.tolist()  #提取评论的值， 并转换成列表

#有些用户为了获取积分或者获取金钱奖励，而采取了一种复制手段。对于这种文本数据，我们通常使用机械词压缩的方式进行处理
# 机械词去重函数
def qc_string(s):
    filelist = s
    filelist2 = []
    for a_string in filelist:
        # 将文本翻转
        temp = a_string[::-1]
        char_list = list(temp) #把字符串转化列表自动按单个字符分词了
        list1 = []#原始文本
        list1.append(char_list[0])
        list2 = ['']#比较文本
        del1 = []#记录要删除的索引
        i = 0
        while (i<len(char_list)):
            i = i + 1
            #若i为最后一个位置时，list1 与list2文本相同，需要删除的文本索引为range(i-m,i)，其中m为list2的总字符数
            if i == len(char_list):
                if list1 == list2:
                    m = len(list2)
                    for x in range(i-m, i):
                        del1.append(x)
            else:
                #(1.1)若词汇与list1第一个词汇相同，list2为空，将词加入list2中
                if char_list[i] == list1[0] and list2 == ['']:
                    list2[0] = char_list[i]
                #(1.2)若词汇与list1第一个词汇相同，list2不为空，分两种情况：
                elif char_list[i] == list1[0] and list2 != ['']:
                #(1.2.1)若list1=list2，记录要删除的索引位置，并重置list2，将新的词汇复制给list2
                    if list1 == list2:
                        m = len(list2)
                        for x in range(i-m, i):
                            del1.append(x)
                        list2 = ['']
                        list2[0] = char_list[i]
                    #(1.2.2)若list1不等于list2，令list1=list2，并重置list2，将新的词汇复制给list2
                    else:
                        list1 = list2
                        list2 = ['']
                        list2[0] = char_list[i]
                #(2.1)若词汇和list1第一个词汇不同，list2为空，将词加入list1'
                elif char_list[i] != list1[0] and list2 == ['']:
                    list1.append(char_list[i])
                #(2.2)若词汇和list1第一个词汇不同，list2不为空，分两种情况：
                elif char_list[i] != list1[0] and list2 !=['']:
                    #(2.2.1)如果list1等于list2且list2的字符长度大于2，则记录要删除的索引位置，并重置list1，list2
                    if list1 == list2 and len(list2) >= 2:
                        m = len(list2)
                        for x in range(i-m, i):
                            del1.append(x)
                        list1 = ['']
                        list1[0] = char_list[i]
                        list2 = ['']
                    #(2.2.2)如果list1不等于list2，将新的词汇加入到list2中
                    else:
                        list2.append(char_list[i])
        #将位置索引进行排序
        a = sorted(del1)
        t = len(a)-1
        while t >= 0:
            del char_list[a[t]]
            t = t - 1
        str1 = ''.join(char_list)
        str2 = str1.strip()
        str2 = str2[::-1]
        filelist2.append(str2)
    return filelist2

# 将DataFrame中的评论提取出来进行机械词压缩处理：
list_goods = goods.评论.values.tolist()
res = qc_string(list_goods)

#print(res)

# 用户为了方便，直接复制别人的评价，删除一模一样的评论。
res1 = []
for i in res:
    if i not in res1:
        res1.append(i)
# 在进行停留词以及无意义词汇处理时，需要先对用户文本数据进行分词才能处理。选用Python中的Jieba分词来对文本进行分词。
import jieba
#导入停留词，文件路径为相对路径（可以将一些没意义的词语写写入停留词文本，后面在重新分词将其跳过，词频图就不会出现了）
stopwords = pd.read_table("/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/stopwords.txt",
                          quoting=3, names=['stopword']) #names参数为添加的字段名
#将停留词转换成列表
stopwords_list = stopwords.values.tolist()

#对评论文本进行分词，遍历每一个词，如果该词出现停留词列表中就跳过。
text = ''
for i in res1:
    jieba.load_userdict(
        "/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/mydict.txt")
    # 加载自定义词典，保证双十一被正确地分词了。
    seg = jieba.lcut(i)
    for word in seg:
        if word in stopwords_list:
            continue
        else:
            text = text + ' ' + word
print(text)
#break和continue：break语句和continue语句的区别：break语句是结束整个循环的过程，不在判断执行循环的条件是否成立；continue语句是只结束本次循环，并不终止整个循环的执行
#break：用来跳出最内层的for循环或者while循环，脱离该循环后程序从循环代码后面继续执行。即break语句只能跳出当前层次的循环。
#continue：结束当前当次循环，即跳出循环体中还没有执行的语句，但是并不跳出当前循环。
#pass:不做任何作用，只起到占位的作用。循环中使用 pass 不会跳出循环
#for循环和while循环中的else扩展用法:else中的程序只在一种条件下执行，即循环正常遍历所有内容或者由于条件不成立而结束循环，没有因break或者return而退出循环。continue对else没有什么影响

# 词频分析
# 导入绘图包pyplot和词云包WordCloud。
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# 配置词云的基本参数。
my_cloud = WordCloud(
background_color='white',#背景色为白色
font_path='/System/Library/fonts/PingFang.ttc',#词云字体为宋体 windows电脑字体设置路径为'C:/Windows/Fonts/simsun.ttc',#词云字体为宋体
width=1000,
height=500)
# 用分好的词进行词云的生成。
my_cloud.generate(text)
# 显示词云
plt.rcParams['figure.figsize'] = (10, 6)#图片宽10inch，高6inch
plt.imshow(my_cloud, interpolation='bilinear')#为了提升图片清晰度，此处设置双线
# 性插值对图像进行优化处理'bilinear'
# 隐藏坐标轴
plt.axis('off')
plt.show()
#通过词频分析，我们发现用户最关注的是商品的效果、商品的性价比(价格、划算、买二送)
#注意：电商网站中的活动是"双十一"，而分词的结果为"双十"，遇到这种情况可以在分词前创建一个自定义的词典，使得分词更合理
#文本文件的编码方式必须为utf—8,用系统自带的记事本工具中输入分词的字典即可


#5提出文本主题
#文本主题提取即提取主题关键词，而能够体现文本内容主题的关键词就称为主题关键词。
#文本主题提取的方法主要有两个：1。TF-IDF模型 2。LDA主题模型。此处我们选用TF-IDF模型对文本进行主题对提取
#TF-IDF模型对核心思想：如果某个词语或短语在一篇文章中出现的TF频率高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类
# 实现方法：jieba分词包中含有analyse模块，在进行关键词提取时可以使用下列方法：jieba.analyse.extract_tags(sentence, topK,withWeight=True) 其中sentence为待提取的文本，topK为返回几个TF/IDF权重最大的关键词，默认值为20。
import jieba.analyse
TF_IDF = jieba.analyse.extract_tags(text, topK=10, withWeight=True)
print(TF_IDF)