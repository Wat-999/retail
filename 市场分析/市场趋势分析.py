#数据清洗思路
#1首先应该进行的数据整理是对7个子行业数据进行整合合并
#2其次应该进行对是时间年度对整合。原因是，在电商行业中，如果要进行市场潜力对分析，那么通常会选择整个年度作为时间分析跨度。而此处对数据中，2015年
#与2018年都不是完整年度，需要对数据进行补齐。对该数据集，我们选用回归预测将2018年11月与12月对数据补齐

import pandas as pd

dwx = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/电蚊香套装市场近三年交易额.xlsx')
fmfz = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/防霉防蛀片市场近三年交易额.xlsx')
msmc = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/灭鼠杀虫剂市场近三年交易额.xlsx')
mz = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/盘香灭蟑香蚊香盘市场近三年交易额.xlsx')
wxq = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香加热器市场近三年交易额.xlsx')
wxp = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香片市场近三年交易额.xlsx')
wxy = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香液市场近三年交易额.xlsx')


#将每个表格中3年对交易额数据根据时间进行合并
d = pd.merge(dwx, fmfz, on='时间') #on参数用于连接的列名，必须同时存在于左右两个DataFrame对象中，如果未指定，则以left和right列名的交集作为连接键
for i in [msmc, mz, wxq, wxp, wxy]:
    d = pd.merge(d, i, on='时间')
d.columns = ['时间', '电蚊香', '防霉防蛀', '灭鼠灭虫', '灭蟑', '蚊香加热器', '蚊香片', '蚊香液']

#观察数据
#print(d.head()) #前5行
#print(dwx.tail())  #后5行

#补齐缺失月对数据
#数据时间宽度是2015年11月到2018年10月，从时间到完整性来讲，虽然是36个月，但不是完整到3年。这种情况下就要根据分析场景与业务方沟通对"年"的定义
#可以按照类似"财年"的概念来分析，每12个月为一年。如果业务方需要按照西历定义的"年"来分析，则需要补齐缺失的两个月的数据，取2016年1月到2018年12月，共计36个月到数据
#如果可以直接获取到2018年11月和12月到数据当然最好，但在实际工作中可能接到任务时还是2018年的11月。如果你跟老板说我们要等到2019年1月才能开始分析，
#因为那时才能拿到完整的数据，那么你很可能就被老板炒了。这种情况可以使用预测的方法，预测出2018年11月和12月的数据，然后用预测的数据进行分析。

#索引2015，2016， 2017年12月的数据
t17 = d.where(d.时间 == '2017-12-01').dropna() #dropna()用来删除含空值的行和列
t16 = d.where(d.时间 == '2016-12-01').dropna()
t15 = d.where(d.时间 == '2015-12-01').dropna()

#将索引出的数据进行合并
t4 = pd.concat([t17, t16, t15])
#print(t4)

#由于我们的目的是用2015——2017年这3年的12月的数据来进行回归建模，预测2018年12月的数据，因此，此处我们选用2015、2016、2017作为x变量，每一年12月的数据作为y变量
y = t4.drop('时间', axis=1)
#设置x轴的年份
x = [2017, 2016, 2015]

#使用回归算法预测，先加载Numpy和sklearm库
import numpy as np
from sklearn import linear_model

#先将数据处理成回归模型所需要的形式（#由于sklearn接受的是numpy数组，所以又是需要处理数据，）
x_train = np.array(x).reshape(-1, 1)
y_train = np.array(y.iloc[:, 0])  #iloc[:, 0]表示所有行，0列即行本身这列

# reshape(-1,1)中的-1代表无意义
# reshape(-1,1)代表将二维数组重整为一个一列的二维数组
# reshape(1,-1)代表将二维数组重整为一个一行的二维数组
# reshape(-1,n)代表将二维数组重整为n列的二维数组
# reshape(n,-1)代表将二维数组重整为n行的二维数组

#将线性模型实例化
linear_reg = linear_model.LinearRegression()

#搭建模型
linear_reg.fit(x_train, y_train)

#输入自变量2018，预测2018年12月的销售额
y_2018_12 = linear_reg.predict(np.array([2018]).reshape(-1, 1)).round(1)
print(y_2018_12[0])  #因为是列表，所以哪怕是一个值也只能采用提取

#当一个动作有规律地出现3次或3次以上时，肯定有一个办法可以高效、便捷地实现，采用循环来预测
y_12 = []
for i in range(7):
    y_train = np.array(y.iloc[:, i])
    linear_reg = linear_model.LinearRegression()
    linear_reg.fit(x_train, y_train)
    y_pre = linear_reg.predict(np.array([2018]).reshape(-1, 1)).round(1)
    y_12.append(y_pre[0])
print(y_12)

#下面预测11月的数据
t1 = d.where(d.时间 == '2017-11-01').dropna() #dropna()用来删除含空值的行和列
t2 = d.where(d.时间 == '2016-11-01').dropna()
t3 = d.where(d.时间 == '2015-11-01').dropna()

#将索引出的数据进行合并
t = pd.concat([t1, t2, t3])
#选用每一年11月的数据作为y变量
y1 = t.drop('时间', axis=1)

#预测2018年所有子行业11月的预测值
y_11 = []
for i in range(7):
    y1_train = np.array(y1.iloc[:, i])
    linear_reg = linear_model.LinearRegression()
    linear_reg.fit(x_train, y1_train)
    y_pre = linear_reg.predict(np.array([2018]).reshape(-1, 1)).round(1)
    y_11.append(y_pre[0])
print(y_11)

#3整理数据集
#预测好的数据要写回到数据集，删除2015年两个月的数据，并且修改好日期的格式。在绘制图形前，还需要根据时间汇总数据，如按年或者季度汇总

#添加2018年11月和12月的数据
import datetime

a1 = datetime.datetime.strptime('2018-11-1', '%Y-%m-%d')   #将字符串转为datetime格式
a2 = datetime.datetime.strptime('2018-12-1', '%Y-%m-%d')
y_11.insert(0, a1)  #插入数据
y_12.insert(0, a2)
#insert()函数用于将指定对象插入列表的指定位置,第一个参数为索引的位置，第二个参数为插入的对象

#将2015年11月和12月的数据替换成预测结果，2015年11月12月的数据可以通过观察数据集读取行号精准定位
d.iloc[34] = y_12
d.iloc[35] = y_11
print(d.tail()) #查看替换成功

#按照日期降序排列
d.sort_values(by='时间', ascending=False, inplace=True)

#重置索引
d.reset_index(inplace=True)

#由于之前的索引列没有作用，所以删除
del d['index']
#查看数据结果
#print(d.head())

#汇总每一个月份的子行业市场数据
d2 = d.drop('时间', axis=1)
d['col_sum'] = d2.apply(lambda x: x.sum(), axis=1)

#提取日期的年份
d['year'] = d.时间.apply(lambda x: x.year)

#按年份汇总数据
data_sum = d.groupby('year').sum()
print(data_sum.index)

#绘制趋势图
import matplotlib.pyplot as plt

#设置参数，以确保图形正确显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

#将年份设置为x轴， 将汇总的驱虫剂市场总交易额作为y轴
year = list(data_sum.index)  #将其索引转换为列表，因为其索引为年份
x = range(len(year))
y = data_sum['col_sum']
#选择ggplot的绘图方式
with plt.style.context('ggplot'):
    # 设置画布大小宽8inch，高6inch。
    pl = plt.figure(figsize=(8, 6))
    # 绘制线图。
    plt.plot(x, y)
    # 设置图表标题，x轴标题，y轴标题，设置刻度线格式。
    plt.title('近三年驱虫市场趋势图', fontsize=20, pad=20)  #其中pad参数为标题到表格到距离
    plt.xlabel('year')
    plt.ylabel('交易额')
    plt.xticks(x, year, fontsize=9, rotation=45)  # 第一个参数x代表x坐标轴的位置，第二个参数year代表x坐标轴的位置的显示lable即标签，  rotation=45表示横轴逆时针选择45度

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
    for a, b in zip(x, data_sum.iloc[:, 2]):  #会比设置显示列数字标签，多一列用来参考(一般在正中间多那条线）
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)

    # 设置数字标签。
    for a, b in zip(x, data_sum.iloc[:, 6]):  #会比设置显示列数字标签，多一列用来参考(一般在正中间多那条线）
        plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
    plt.plot(x, data_sum.iloc[:, 3])
    plt.plot(x, data_sum.iloc[:, 4])
    plt.plot(x, data_sum.iloc[:, 5])
    plt.plot(x, data_sum.iloc[:, 6])
    # 设置图的标题，x轴标题，y轴标题，设置刻度线格式。
    plt.title('近三年驱虫市场各子市场容量趋势')
    plt.xlabel('year')
    plt.ylabel('交易额')
    plt.xticks(x, year, fontsize=9, rotation=45)
    # 设置图例，
    plt.legend(['电蚊香', '防霉防蛀', '灭鼠灭虫', '灭蟑', '蚊香加热器', '蚊香片', '蚊香液'])
    plt.show()

#绘制各个子行业占比趋势图
#计算每一个子行业的占比
data_percentage = data_sum.copy()  #复制数据集将其赋值
for i in range(3):
    data_percentage.iloc[i] = round(data_percentage.iloc[i]/data_percentage.iloc[i][-1]*100, 2)
del data_percentage['col_sum']
#print(data_percentage)


#绘制驱虫剂市场各子行业占比趋势图
with plt.style.context('ggplot'):
    # 设置画布大小宽8inch，高6inch。
    pl = plt.figure(figsize=(8, 6))
    # 绘制各叶子行业市场趋势线图。
    plt.plot(x, data_percentage.iloc[:, 0])
    plt.plot(x, data_percentage.iloc[:, 1])
    plt.plot(x, data_percentage.iloc[:, 2])
    # 设置数字标签。
    for a, b in zip(x, data_percentage.iloc[:, 2]):  # 会比设置显示列数字标签，多一列用来参考(一般在正中间多那条线）
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)

    # 设置数字标签。
    for a, b in zip(x, data_percentage.iloc[:, 6]):  # 会比设置显示列数字标签，多一列用来参考(一般在正中间多那条线）
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
    plt.plot(x, data_percentage.iloc[:, 3])
    plt.plot(x, data_percentage.iloc[:, 4])
    plt.plot(x, data_percentage.iloc[:, 5])
    plt.plot(x, data_percentage.iloc[:, 6])
    # 设置图的标题，x轴标题，y轴标题，设置刻度线格式。
    plt.title('近三年驱虫市场各子市场容量趋势')
    plt.xlabel('year')
    plt.ylabel('交易额')
    plt.xticks(x, year, fontsize=9, rotation=45)
    # 设置图例，
    plt.legend(['电蚊香', '防霉防蛀', '灭鼠灭虫', '灭蟑', '蚊香加热器', '蚊香片', '蚊香液'])
    plt.show()  #由上述分析可知"灭鼠灭虫"沙场市场一直位居首位，近三年来，占比均在60%以上，可以说该子行业增长态势优良，规模的天花板足够高

#计算市场增量
#市场增量分析即增量分析法，是指对被比较市场在规模、成本等方面等差额部分进行分析，进而对市场进行比较
#将"灭鼠灭虫"市场近三年的销售数据索引出来
d_m = list(data_sum['灭鼠灭虫'].round(2))

#计算2017年的环比增幅
print((d_m[1] - d_m[0])/d_m[0])
#计算2018年的环比增幅
print((d_m[2] - d_m[1])/d_m[1])
#增量计算也可以使用pct_change()方法，该方法会计算当前数据和上一个数据的差值比例
print(data_sum['灭鼠灭虫'].pct_change())





# 绘制组合图
# 组合图是将两种以上的图形类型叠加在一起，只要坐标系相同就可以叠加，如柱形图和折线图，Python提供了灵活的图形组合功能。
d_p = data_sum.apply(lambda x: x/100000000, axis=0).round(2)  #换算单位为亿
with plt.style.context('ggplot'):
    pl = plt.figure(figsize=(8, 6))
    # 绘制柱状图。
    plt.bar(x, d_p.iloc[:, 2])
    # 绘制线图，color='b'表示图形的颜色渲染成蓝色（blue），marker表示标记用o标记。
    plt.plot(x, d_p.iloc[:, 2], color='b', marker='o')

    # 设置图标题、坐标轴标题，并画图
    for a, b in zip(x, d_p.iloc[:, 2]):
        plt.text(a, b+0.05, '%.2f' % b, ha='center', va='bottom', fontsize=8)
    plt.title('近三年灭鼠杀虫市场容量趋势(亿元)')
    plt.xlabel('year')
    plt.ylabel('交易额')
    plt.xticks(x, year, fontsize=9, rotation=45)
    plt.show()