def qc_string(s):
    filelist2 = []
    for filelist in s:
        char = list(filelist)
        #char = list('刚收到，家里厨房突然出现小强了，看了这个评价挺多挺好，销量也大，赶紧定了三盒，一定要管用啊一定要管用，一定要管用，准备看下后续效果会继续追加评价。不知道多久才能消灭干净，还在厨房，没法做饭了，都不愿意进去了。有点担心会挥发。看很多人在用也就试试吧。哎哎哎哎哎哎哎哎哎哎哎哎哎哎哎哎哎哎')
        list1 = []
        list1.append(char[0])
        list2 = ['']
        del1 = []
        i = 0
        while (i < len(char)):
            i = i + 1
            if i == len(char):
                break
            elif char[i] == list1 and list2 == ['']:
                list2 = char[i]
            elif char[i] == list1 and list2 != ['']:
                if char[i] == list1 and list1 == list2[-1]:
                    del1.append(i)
                else:
                    list2 = char[i]
            elif char[i] != list1:
                list1 = char[i]
        a = sorted(del1)
        t = len(a) - 1
        while (t >= 0):
            del char[a[t]]
            t = t - 1
        str1 = ''.join(char)
        str2 = str1.strip()
        filelist2.append(str2)
    return filelist2

list_goods = goods.评论.values.tolist()
res = qc_string(list_goods)
