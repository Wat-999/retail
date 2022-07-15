import pandas as pd

dwx = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/电蚊香套装市场近三年交易额.xlsx')
fmfz = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/防霉防蛀片市场近三年交易额.xlsx')
msmc = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/灭鼠杀虫剂市场近三年交易额.xlsx')
mz = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/盘香灭蟑香蚊香盘市场近三年交易额.xlsx')
wxq = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香加热器市场近三年交易额.xlsx')
wxp = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香片市场近三年交易额.xlsx')
wxy = pd.read_excel('/Users/macbookair/Desktop/数据分析/书本配套资料及电子书/python商业数据分析(零售和电子商务)/《Python商业数据分析：零售和电子商务案例详解》/第三章Python与市场分析案例/电商案例数据及数据说明/驱虫剂市场/蚊香液市场近三年交易额.xlsx')

#观察数据
#print(dwx.head()) #前5行
#print(dwx.tail())  #后5行

#查看数据结构
#print(dwx.info())

#通过对数据对探索与观察，数据集是7个子行业数据，每个子行业对数据中一共有两列字段：时间和交易金额，
#用sum()方法汇总总数据
#dwx['交易金额'].sum() #汇总单张表格数据


#将七张表格的数据汇总并形成一张表
m_sum = pd.DataFrame(data=[dwx.sum().values, fmfz.sum().values, msmc.sum().values,
                           mz.sum().values, wxq.sum().values, wxp.sum().values, wxy.sum().values],
                     columns=['销售额'], index=['电蚊香', '防霉防蛀', '灭鼠灭虫', '灭蟑', '蚊香加热器', '蚊香片', '蚊香液'])
#dwx.sum().values以array形式返回指定sum()的所有取值，循环速度较快
#print(m_sum)

#对上述输出结果进行行汇总，得到驱虫市场总规模
m_sum.loc['Row_sum'] = m_sum.apply(lambda x: x.sum())  #用loc新增一行行汇总，并且行名为['Row_sum']，再用apply传入匿名函数求和
#print(m_sum)  #也可以直接用m_sum.sum()也是新增一行汇总求和，但是不方便后期调用数据

#计算市场相对规模(新增一列)
#m_sum['份额占比'] = m_sum/m_sum.loc['Row_sum']

#将份额占比调整为百分比，保留一位小数。可以使用函数round：round（number，ndigits=None）第一个参数为数字，第二个参数为保留几位小数点
m_sum['份额占比'] = round(m_sum/m_sum.loc['Row_sum']*100, 1)

#再将最后一行删除Row_sum删除
#m_sum.dorp(labels=['Row_sum'], axis=0, inplace=True)  #labels用于指定具体行名称或列名称某一个数值
m_sum.drop(index=['Row_sum'], axis=0, inplace=True)   #同上,这里是用于指定行名称，如果是列用columns
#print(m_sum)

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
#zip([seq1, ...])接受一系列可迭代对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。若传入参数的长度不等，则返回列表的长度和参数中长度最短的对象相同。
#zip(x, y)中的x，y值代表不同柱子的坐标位置，for循环遍历每一个x，y，使用plt.text()在对应位置添加文字说明生成数字标签
#其中a, b+0.05,表示在每一柱子对应的x值、y值上方0.05处标注文字说明；
#'%.0f' % b,表示标注的文字格式，比如，%.3f表示保留3位小数，这里即表示保留0位小数，即整数
#ha='center', va='bottom',表示horizontalalignment（水平对齐）的对齐方式为center（居中）、verticallignment（垂直对齐）的对齐方式为bottom（底部）
#fontsize=8表示设置字号为8

#用市场相对份额绘制饼图
#将子行业名称设置为饼图的标签，相对市场份额设置饼图的大小
labels = m_sum.index.values.tolist()
sizes = m_sum['份额占比'].values.tolist()

#设置画布的宽为8， 高为6
pl = plt.figure(figsize=(10, 6))
#绘制饼图
plt.pie(sizes, labels=labels, autopct='%.1f%%', shadow=False, startangle=180)
#labels参数不同数据对应的标签
#autopct='%.1f%%',表示设置百分比的格式，此处保留1位小数，f后面的两个%表示实际显示数字的百分号
#startangle=180表示设置饼图的初始角度
#设置标题
plt.title('子市场相对市场份额')

#设置饼图为圆形
plt.axis('equal')
plt.show()
