"""
    ======================================================
    =================市场大盘容量分析==================
    ======================================================
"""

import pandas as pd

# 文件路径为python文件位置下的相对路径
dwx = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/电蚊香套装市场近三年交易额.xlsx')
fmfz = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/防霉防蛀片市场近三年交易额.xlsx')
msmc = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/灭鼠杀虫剂市场近三年交易额.xlsx')
mz = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/盘香灭蟑香蚊香盘市场近三年交易额.xlsx')
wxq = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香加热器市场近三年交易额.xlsx')
wxp = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香片市场近三年交易额.xlsx')
wxy = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香液市场近三年交易额.xlsx')

# 使用head()方法查看前5行数据
#print(dwx.head())
# 使用tail()方法查看后5行数据
#print(dwx.tail())
# 使用info()方法查看数据的字段及类型
dwx.info()
# 用sum方法汇总数据
dwx['交易金额'].sum() #汇总单张表格数据
# 将7张表格的数据汇总并形成一张表
m_sum = pd.DataFrame(data=[dwx.sum().values, fmfz.sum().values, msmc.sum().values,
                           mz.sum().values, wxq.sum().values, wxp.sum().values, wxy.sum().values],
                     columns=['销售额'], index=['电蚊香', '防霉防蛀', '灭鼠灭虫', '灭蟑', '蚊香加热器', '蚊香片', '蚊香液'])
#print(m_sum)
# 对上述数据进行行汇总，得到驱虫市场总规模
m_sum.loc['Row_sum'] = m_sum.apply(lambda x: x.sum())
# 或者m_sum ['Col_sum'] = m_sum.sum()
#print(m_sum)
# 在上一节的基础上计算相对规模
#m_sum['份额占比'] = m_sum/m_sum.loc['Row_sum']
#print(m_sum)
# 将份额占比调整为百分比，保留1位小数
# 使用函数round: round(number, ndigits=None),第一个参数为数字，第二个参数为保留几位小数。
m_sum['份额占比'] = round(m_sum/m_sum.loc['Row_sum']*100, 1)
# 并将最后一行Row_sum删除
m_sum.drop(labels=['Row_sum'], axis=0, inplace=True)
print(m_sum)
#绘制柱状图和饼图
import matplotlib.pyplot as plt

#设置参数，以确保图形正确显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

#将子行业的名称设置为X轴， 子行业的绝对份额设置为y轴
x = m_sum.index.values.tolist()  #tolist()函数将外层，内层全部转换为list类型
y = m_sum['销售额'].values.tolist()

#设置画布大小
pl = plt.figure(figsize=(8, 6)) #表示图片的大小为宽8inch，高为6inch，（单位为inch）

#绘制子市场绝对份额柱状图
plt.bar(x, y)
#设置标题及x轴标题、y轴标题
plt.title('市场绝对份额', fontsize=20, pad=100)  #其中pad参数为标题到表格到距离
plt.xlabel('叶子市场')
plt.ylabel('份额占比')

#设置数字标签
for a, b in zip(x, y):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
plt.show()

# 用市场相对份额绘制饼图
# 将叶子行业名称设置为饼图的标签，相对市场份额设置为饼图的大小
labels = m_sum.index.values.tolist()
sizes = m_sum['份额占比'].values.tolist()

#设置画布的宽为8， 高为6
pl = plt.figure(figsize=(10, 6))
#绘制饼图

# 绘制饼图，autopct='%.1f%%'：# 设置百分比的格式，此处保留1位小数，f后面的两个%表示实际显示数字的百分号，startangle=180# 设置饼图的初始角度。
plt.pie(sizes, labels=labels, autopct='%.1f%%', shadow=False, startangle=180)
# 设置标题
plt.title("叶子市场相对市场份额")
# 设置饼图使得饼图为圆形，如图4-2所示
plt.axis('equal')
plt.show()

"""
    ======================================================
    =================市场大盘趋势分析==================
    ======================================================
"""

# 根据时间合并市场数据
d = pd.merge(dwx, fmfz, on='时间')
for i in [msmc, mz, wxq, wxp, wxy]:
   d = pd.merge(d, i, on='时间')
d.columns = ['时间', '电蚊香', '防霉防蛀', '灭鼠灭虫', '灭蟑', '蚊香加热器', '蚊香片', '蚊香液']
# 先使用head()和tail()方法观察数据
d.head()
d.tail()
# 补齐缺失月份数据
# 预测一个叶子行业的12月数据
# 索引2017年12月分数据
t17 = d.where(d.时间 == '2017-12-1').dropna()
# 同理将2016年12月和2015年12月的数据也索引出来
t16 = d.where(d.时间 == '2016-12-1').dropna()
t15 = d.where(d.时间 == '2015-12-1').dropna()
# 将2015年，2016年，2017年三年的数据合并
t4 = pd.concat([t17, t16, t15])
# 由于我们的目的是用2015-2017年3年的12月份数据来进行回归建模，预测2018年12月数据
# 因此，此处我们选用2015,2016,2017作为x变量，每一年12月份的数据作为y变量
y = t4.drop('时间', axis=1)
# 设置x轴的年份。
x = [2017, 2016, 2015]
# 使用回归算法预测，先加载numpy和sklearn库。
import numpy as np
from sklearn import linear_model
# 将数据处理成回归模型所需要的形式。
x_train = np.array(x).reshape(-1, 1)
y_train = np.array(y.iloc[:, 0])
# 将线性模型实例化。
linear_reg = linear_model.LinearRegression()
# 搭建模型。
linear_reg.fit(x_train, y_train)
# 输入自变量2018，预测2018年12月份的销售额。
y_2018_12 = linear_reg.predict(np.array([2018]).reshape(-1, 1)).round(1)
# 输出预测结果。
print(y_2018_12[0])
# 当一个动作有规律的出现3次或以上，肯定有一个办法可以更高效便捷。
# 用循环预测所有叶子行业的12月数据
# 写FOR循环，得到2018年所有类目12月份的预测值。
y_12 = []
for i in range(7):
 y_train = np.array(y.iloc[:, i])
 linear_reg = linear_model.LinearRegression()
 linear_reg.fit(x_train, y_train)
 y_pre = linear_reg.predict(np.array([2018]).reshape(-1, 1)).round(1)
 y_12.append(y_pre[0])
# 打印2018年个叶子行业12月份的预测结果。
print(y_12)
# 预测11月的数据
# 提取2015到2017年11月的数据。
t1 = d.where(d.时间 == '2017-11-1').dropna()
t2 = d.where(d.时间 == '2016-11-1').dropna()
t3 = d.where(d.时间 == '2015-11-1').dropna()
t = pd.concat([t1, t2, t3])
y1 = t.drop('时间', axis=1)
# 写FOR循环，得到2018年所有类目11月份的预测值。
y_11 = []
for i in range(7):
 y1_train = np.array(y1.iloc[:, i])
 linear_reg = linear_model.LinearRegression()
 linear_reg.fit(x_train, y1_train)
 y_pre=linear_reg.predict(np.array([2018]).reshape(-1, 1)).round(1)
 y_11.append(y_pre[0])
# 打印2018年叶子行业11月份的预测结果。
print(y_11)

# 整理数据集
# 加载datetime库。
import datetime
# 将字符串转为datetime。
a1 = datetime.datetime.strptime('2018-11-1', '%Y-%m-%d')
# 将数据插入y_11中。
y_11.insert(0, a1)
print(y_11)
# 将字符串转为datetime。
a2 = datetime.datetime.strptime('2018-12-1', '%Y-%m-%d')
y_12.insert(0, a2)
print(y_12)
# 将2015年11月和12月的数据替换成预测的结果，2015年11月和12月的数据可以通过观察数据集读取行号精准定位。
d.iloc[34] = y_12
d.iloc[35] = y_11
d.tail()
# 按照日期降序排序。
d.sort_values(by='时间', ascending=False, inplace=True)
# 重置索引。
d.reset_index(inplace=True)
# 由于“index”列没有作用，可以删除。
del d['index']
# 查看数据结果。
print(d.head())
# 汇总每一个月份的类目市场数据
d2 = d.drop('时间', axis=1)
d['col_sum'] = d2.apply(lambda x: x.sum(), axis=1)
# 提取日期的年份。
d['year'] = d.时间.apply(lambda x: x.year)
# 按年份汇总数据。
data_sum = d.groupby('year').sum()
print(data_sum)

# 绘制趋势图

# 首先导入matplotlib绘图包。
# import matplotlib.pyplot as plt
# 将年份设置为x轴，将汇总的驱虫市场总销售作为y轴。
year = list(data_sum.index)
x = range(len(year))
y = data_sum['col_sum']
# 选择ggplot的绘图方式。
with plt.style.context('ggplot'):
    # 设置画布大小宽8inch，高6inch。
    pl=plt.figure(figsize=(8, 6))
    # 绘制线图。
    plt.plot(x, y)
    # 设置图表标题，x轴标题，y轴标题，设置刻度线格式。
    plt.title('近三年驱虫市场趋势图')
    plt.xlabel('year')
    plt.ylabel('交易额')
    plt.xticks(x, year, fontsize=9, rotation=45)  # rotation=45表示横轴逆时针选择45度
    # 展示趋势图，如图4 - 3
    # 所示，市场呈现增长趋势。
    plt.show()

# 绘制各个叶子市场的趋势图
with plt.style.context('ggplot'):
    # 设置画布大小宽8inch，高6inch。
    pl = plt.figure(figsize=(8, 6))
    # 绘制各叶子行业市场趋势线图。
    plt.plot(x, data_sum.iloc[:, 0])
    plt.plot(x, data_sum.iloc[:, 1])
    plt.plot(x, data_sum.iloc[:, 2])
    # 设置数字标签。
    for a, b in zip(x, data_sum.iloc[:, 2]):
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
    plt.plot(x, data_sum.iloc[:, 3])
    plt.plot(x, data_sum.iloc[:, 4])
    plt.plot(x, data_sum.iloc[:, 5])
    plt.plot(x, data_sum.iloc[:, 6])
    # 设置数字标签。
    for a, b in zip(x, data_sum.iloc[:, 6]):
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
    # 设置图的标题，x轴标题，y轴标题，设置刻度线格式。
    plt.title('近三年驱虫市场各子市场容量趋势')
    plt.xlabel('year')
    plt.ylabel('交易额')
    plt.xticks(x, year, fontsize=9, rotation=45)
    # 设置图例，并画图，如图4-4所示。
    plt.legend(['电蚊香', '防霉防蛀', '灭鼠灭虫', '灭蟑', '蚊香加热器', '蚊香片', '蚊香液'])
    plt.show()

# 绘制各个叶子市场占比趋势图
# 计算每一个叶子市场的占比。
data_percentage = data_sum.copy()
for i in range(3):
  data_percentage.iloc[i] = round(data_percentage.iloc[i]/data_percentage.iloc[i][-1]*100, 2)
del data_percentage['col_sum']

# 绘制驱虫市场各子市场占比趋势图
with plt.style.context('ggplot'):
    pl = plt.figure(figsize=(8, 6))
    plt.plot(x, data_percentage.iloc[:, 0])
    plt.plot(x, data_percentage.iloc[:, 1])
    plt.plot(x, data_percentage.iloc[:, 2])
    for a, b in zip(x, data_percentage.iloc[:, 2]):
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
    plt.plot(x, data_percentage.iloc[:, 3])
    plt.plot(x, data_percentage.iloc[:, 4])
    plt.plot(x, data_percentage.iloc[:, 5])
    plt.plot(x, data_percentage.iloc[:, 6])
    for a, b in zip(x, data_percentage.iloc[:, 6]):
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
    plt.title('近三年驱虫市场各子市场占比趋势')
    plt.xlabel('year')
    plt.ylabel('交易额')
    plt.xticks(x, year, fontsize=9, rotation=45)
    plt.legend(['电蚊香', '防霉防蛀', '灭鼠灭虫', '灭蟑', '蚊香加热器', '蚊香片', '蚊香液'])
    plt.show()

# 计算市场增量
# 将灭鼠灭虫市场近三年的销售数据索引出来。
d_m = list(data_sum['灭鼠灭虫'].round(2))
# 计算2017年的环比增幅。
print((d_m[1]-d_m[0])/d_m[0])
# 计算2018年的环比增幅。
print((d_m[2]-d_m[1])/d_m[1])

# 绘制组合图
# 组合图是将两种以上的图形类型叠加在一起，只要坐标系相同就可以叠加，如柱形图和折线图，Python提供了灵活的图形组合功能。
with plt.style.context('ggplot'):
    pl = plt.figure(figsize=(8, 6))
    # 绘制柱状图。
    plt.bar(x, data_sum.iloc[:, 2])
    # 绘制线图，color='b'表示图形的颜色渲染成蓝色（blue），marker表示标记用o标记。
    plt.plot(x, data_sum.iloc[:, 2], color='b', marker='o')
    # 设置图标题、坐标轴标题，并画图
    for a, b in zip(x, data_sum.iloc[:, 2]):
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
    plt.title('近三年灭鼠杀虫市场容量趋势', pad=10) #pad参数用来设置标题与表格的距离
    plt.xlabel('year')
    plt.ylabel('交易额')
    plt.xticks(x, year, fontsize=9, rotation=45)
    plt.show()

"""
    ======================================================
    ===================细分市场分析===================
    ======================================================
"""

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


# 绘制条形图
# 将产品分类设置为条形图的y坐标轴，销售额设置为条形图的x坐标轴
cate = list(data2.index)
value = data2.iloc[:, 0]
# 设置画布大小宽10inch，高6inch
pl = plt.figure(figsize=(10, 6))
# 绘制条形图
plt.barh(cate, value)
# 设置图标题、x轴标题，y轴标题，并绘制图形
plt.title('灭鼠杀虫各类别销售分布')
plt.xlabel('销售额')
plt.ylabel('类别')
plt.show()

# 绘制饼图
# 设置画布
pl = plt.figure(figsize=(8, 6))
# 将类别设置为标签、将份额占比设置为大小
labels = list(data2.index)
sizes = data2["份额占比"].values.tolist()
# 绘制饼图
plt.pie(sizes, labels=labels, autopct='%.1f%%', shadow=False, startangle=180)
# 设置图标题，并绘制图形
plt.title("类别的相对份额占比")
plt.axis('equal')
plt.show()

# 准备数据
# 根据业务理解删除无关字段
d2.drop(['时间', '页码', '排名', '链接', '主图链接', '主图视频链接', '宝贝标题', '下架时间', '旺旺'], axis=1, inplace=True)
# 遍历每一个字段，删除仅包含一种信息的字段
for i in d2.columns:
    if len(d2[i].value_counts()) <= 1:
        del d2[i]
# 缺失值大于90%的字段删除
for i in d2.columns:
    if d2[i].isnull().sum() > d2.shape[0]*0.9:
        del d2[i]
d2.head()

# 价格区间是市场的基础属性，在切割价格区间时需要设定步长，步长的大小要看价格区间的范围以及消费者对价格的敏感度。
# 观察数据集售价字段的范围在0-498元。
d2.describe() #描述性统计

# 定出7个价格区间，前6个价格区间为50元。
databins = [0, 50, 100, 150, 200, 250, 300, 1000]
datalebels = ['0-50', '51-100', '101-150', '151-200', '201-250', '251-300', '300-1000']
d2['价格区间'] = pd.cut(d2['售价'], bins=databins, labels=datalebels, include_lowest=True)
# 计算不同价格区间的销售额、销售额占比，销量，销量占比。
# 删除重复的宝贝ID。
d3 = d2.iloc[list(d2.宝贝ID.drop_duplicates().index), :]
# 分组汇总
bins1 = d3.groupby('价格区间').sum()
bins1['销售额占比']=round(bins1.预估销售额/bins1.apply(lambda x: x.sum())[3]*100, 2)
print(bins1)

# 计算销量占比。
bins1['销量占比'] = round(bins1['销量（人数）']/bins1.apply(lambda x: x.sum())[1]*100, 2)
# 提取bins1中的字段。
bins2 = bins1.loc[:, ['预估销售额', '销售额占比', '销量（人数）', '销量占比']]
# 计算不同价格区间内的宝贝数，宝贝数即商品数量。
bins3 = d3.groupby('价格区间').宝贝ID.nunique()#nunique过滤去重计数
bins2['宝贝数'] = bins3
bins2['宝贝数占比'] = round(bins2['宝贝数']/bins2.apply(lambda x: x.sum())[4]*100, 2)
# 计算一个宝贝分配到的平均销售额。
bins2['一个宝贝分配的销售额'] = round(bins2.预估销售额/bins2.宝贝数, 2)
bins2.sort_values(by='一个宝贝分配的销售额', ascending=False)
print(bins2)

# 减少步长继续细分价格区间
# 提取0-50区间的数据。
mark_50 = d3[d3.售价 < 50]
# 以10作为步长创建价格区间。
databins = [0, 10, 20, 30, 40, 50.1]   #标签比标签边缘小于0.01
datalebels = ['0-10', '11-20', '21-30', '31-40', '41-50']
mark_50['价格区间'] = pd.cut(mark_50['售价'], bins=databins, labels=datalebels,
include_lowest=True)
# 由于每一个价格区间都需要剖析分析，此处将上述价格分析流程封装成函数
def price_mark(data):
    # 计算得到价格区间的销售额、销售额占比、销量、销量占比。
    bins1 = data.groupby('价格区间').sum()
    bins1['销售额占比'] = round(bins1.预估销售额/bins1.apply(lambda x: x.sum())[3]*100, 2)
    bins1['销量占比'] = round(bins1['销量（人数）']/bins1.apply(lambda x: x.sum())[1]*100, 2)
    bins2 = bins1.loc[:, ['预估销售额', '销售额占比', '销量（人数）', '销量占比']]
    # 计算得到宝贝数，宝贝数占比、宝贝分配
    # 分组非重复计数(不同价格区间内的宝贝数)
    bins3 = data.groupby('价格区间').宝贝ID.nunique()
    bins2['宝贝数'] = bins3
    bins2['宝贝数占比'] = round(bins2['宝贝数']/bins2.apply(lambda x: x.sum())[4]*100, 2)
    bins2['一个宝贝分配的销售额'] =round(bins2.预估销售额/bins2.宝贝数, 2)
    res = bins2.sort_values(by='一个宝贝分配的销售额', ascending=False)
    return res
price_mark(mark_50)

# 同理可以深度剖析101-150价格段。
mark2 = d3[(d3.售价 > 100) & (d3.售价 < 150)]
databins = range(100, 151, 10)
datalebels = ['100-110', '111-120', '121-130', '131-140', '141-150']
mark2['价格区间']=pd.cut(mark2['售价'], bins=databins, labels=datalebels,
include_lowest=True)
price_mark(mark2)

# 通过4.5.2分析，不难发现对于101-150价格段中，131-140这个价格段竞争度低，是不错的切入价格段。于是对该价格段的产品需求进一步分析挖掘。
# 准备数据。
mark_select = d2[(d2.售价 > 130) & (d2.售价 < 140)]
# 根据店铺类型分组汇总分数据。
print(mark_select.groupby('店铺类型').sum())
print(mark_select.groupby('适用对象').sum())
print(mark_select.groupby('物理形态').sum())
print(mark_select.groupby('型号').sum())

# 准备数据。
goods = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/产品评论数据.xlsx')

# 数据的探索。
# 先观察数据。
print(goods.head())
print(goods.评论.value_counts())

# 用户购买后未进行评论时，系统会默认生成“此用户没有填写评论”，而这样的信息是无法表述出用户的需求的，故予以删除。
goods = goods[goods.评论 != '此用户没有填写评论!']#删除不需要的=索引需要的
# 索引需要的数据后，索引并没有发生改变，故重置下索引
goods.reset_index(inplace=True)
# 重置索引后，原有的索引会作为新的列添加到dataframe中，故删除该列。
del goods['index']
# 些用户为了获取积分或者获取金钱奖励，而采取的一种复制手段。处理这种文本数据通常我们使用机械词压缩的方式处理
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
        while i < len(char_list):
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
                elif char_list[i] != list1[0] and list2 != ['']:
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
            t = t-1
        str1 = ''.join(char_list)
        str2 = str1.strip()
        str2 = str2[::-1]
        filelist2.append(str2)
    return filelist2

# 将DataFrame中的评论提取出来进行机械词压缩处理：
list_goods=goods.评论.values.tolist()
res = qc_string(list_goods)

# 用户为了方便，直接复制别人的评价，删除一模一样的评论。
res1 = []
for i in res:
    if i not in res1:
        res1.append(i)

# 在进行停留词以及无意义词汇处理时，需要先对用户文本数据进行分词才能处理。选用Python中的Jieba分词来对文本进行分词。
import jieba
#导入停留词，文件路径为相对路径
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
            text = text + ' ' +word

# 词频分析
# 导入绘图包pyplot和词云包WordCloud。
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# 配置词云的基本参数。
my_cloud = WordCloud(
background_color='white',#背景色为白色
font_path='/System/Library/fonts/PingFang.ttc',#词云字体为宋体
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


# 实现方法：jieba分词包中含有analyse模块，在进行关键词提取时可以使用下列方法：jieba.analyse.extract_tags(sentence, topK,withWeight=True) 其中sentence为待提取的文本，topK为返回几个TF/IDF权重最大的关键词，默认值为20。
import jieba.analyse
TF_IDF = jieba.analyse.extract_tags(text, topK=10, withWeight=True)
print(TF_IDF)