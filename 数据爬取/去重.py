# 导入pandas包并重命名为pd
import pandas as pd
import os
import numpy as np

def reduce_data(path):
    # 读取Excel中Sheet1中的数据
    try:
        data = pd.DataFrame(pd.read_excel(path, 'Sheet1', header=None))
    except:
        data = pd.DataFrame(pd.read_excel(path, 'Sheet', header=None))


    # 删除有空值的行
    data.dropna(axis=0, how='any', inplace=True)

    # 查看去除重复行的数据
    no_re_row = data.drop_duplicates()
    #去除噪声数据
    for i in no_re_row.index:
        row = no_re_row.loc[i]  # loc是根据df的行索引名称来加载的（行名称列名称），iloc是根据行索引顺序来加载的（行数列数）
        if len(row[0]) < 5:
            print(row[0])
            print(i)
            no_re_row.drop(i, axis=0, inplace=True)
            # df.drop(index = [i],axis=0,inplace=True)

    # 查看基于[物品]列去除重复行的数据
    # wp = data.drop_duplicates(['物品'])
    # print(wp)

    # 将去除重复行的数据输出到excel表中
    no_re_row.to_excel(path,index=None,header=None)
    print(path+"处理成功！！！")

def process_data():
    paths = os.listdir(os.getcwd())
    for i in paths:
        if '.' in i:
            pass
        else:
            for j in os.listdir(i):
                path = os.path.join(i,j)
                reduce_data(path)
process_data()

def caculate_size():
    type_list = ['财经','房产','教育','科技','军事','汽车','体育','游戏','娱乐','其他']
    num_list = np.zeros(10).tolist()
    paths = os.listdir(os.getcwd())
    for i in paths:
        if '.' in i:
            pass
        else:
            for j in os.listdir(i):
                path = os.path.join(i,j)
                df = pd.read_excel(path, 'Sheet1', header=None)
                name = j.split('.')[0]
                num_list[type_list.index(name)] += df.shape[0]
    for i in range(len(type_list)):
        print(type_list[i]+'总长度：'+str(num_list[i]))
caculate_size()
