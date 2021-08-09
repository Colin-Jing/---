import pandas as pd
import os
import numpy as np
from sklearn.utils import shuffle
# 将最后整体数据打乱
def daluan(path):
    df = pd.read_excel(path)
    df = shuffle(df)
    df.to_excel('整体数据.xlsx',index=False)

# 得到数据的路径名
def get_data():
    path_list = []
    paths = os.listdir(os.getcwd())
    for i in paths:
        if '.' in i:
            pass
        else:
            for j in os.listdir(i):
                path = os.path.join(i,j)
                path_list.append(path)
    return path_list

# 将所有数据拼接在一起
def main():
    df = pd.DataFrame(columns=['标题','分类'])
    path_list = get_data()
    for path in path_list:
        try:
            tem_data = pd.read_excel(path, 'Sheet', header=None)
            tem_data.columns = ['标题', '分类'] # 如果不指定列索引，则原来的列索引为 0 ，1，合并时就会有问题
        except:
            tem_data = pd.read_excel(path, 'Sheet1', header=None)
            tem_data.columns = ['标题', '分类']
        if '汽车' in path:
            tem_data = tem_data.loc[int(tem_data.shape[0]/2):tem_data.shape[0]]
        if '科技' in path:
            tem_data = tem_data.loc[0:int(tem_data.shape[0]/3*2)]
        if '其他' in path:
            tem_data = tem_data.loc[0:int(tem_data.shape[0]/3)]
        df = pd.concat([df, tem_data], axis=0, join='outer', ignore_index=True)
        print(path+"处理成功！！！")

    df.to_excel('原始数据.xlsx',index=None)#,header=['标题','分类']

# 导出开源数据集的财经数据
def caijing():
    # 导入数据

    df = pd.read_excel(r'C:\Users\Colin_Jing\competition\中国软件杯\1617241934831197.xlsx', sheet_name=0)
    print(df.keys())
    print(df.head())

    title_train_df = df.loc[0:4000, ['title', 'channelName']]

    # 生成训练集
    title_train_df.to_excel(r'光明网/财经.xlsx', index=False,header=None)
#caijing()

# 对数据进行清晰，去除重复的数据，同时删除噪声数据
def reduce_data(path):
    # 读取Excel中Sheet1中的数据
    try:
        data = pd.DataFrame(pd.read_excel(path,'Sheet1')) # header 只能代表列索引，column代表列索引名称
    except:
        data = pd.DataFrame(pd.read_excel(path, 'Sheet'))


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

    # 查看基于[物品]列去除重复行的数据
    # wp = data.drop_duplicates(['物品'])
    # print(wp)

    # 将去除重复行的数据输出到excel表中
    no_re_row.to_excel(path,index=False)
    print(path+"处理成功！！！")



#将开源数据集中的教育与爬取数据相结合
def final(path):
    df = pd.read_excel('整体数据.xlsx')
    try:
        tem_data = pd.read_excel(path, 'Sheet')
        tem_data.columns = ['标题', '分类'] # 如果不指定列索引，则原来的列索引为 0 ，1，合并时就会有问题
    except:
        tem_data = pd.read_excel(path, 'Sheet1')
        tem_data.columns = ['标题', '分类']
    tem_data = tem_data.loc[0:8000]
    df = pd.concat([df, tem_data], axis=0, join='outer', ignore_index=True)
    print(path+"处理成功！！！")

    df.to_excel('整体数据.xlsx',index=None)#,header=['标题','分类']
    print('数据保存成功！！！')



# 更新最后数据的标签
def updata_label(path):
    # 标签更新
    label_list = ['财经', '房产', '教育', '科技', '军事', '汽车', '体育', '游戏', '娱乐', '其他']
    tmp_file = pd.read_excel(path)
    #
    for k in range(len(label_list)):
        for i in range(len(tmp_file['分类'])):
            if tmp_file['分类'][i] == label_list[k]:
                tmp_file['分类'][i] = k
    tmp_file.to_excel(path, index=False)


# 整合
main()
# 对整合后的数据进行清洗
reduce_data('原始数据.xlsx')
# 打乱顺序
daluan('原始数据.xlsx')
# 添加教育数据
final(r'C:\Users\Colin_Jing\competition\中国软件杯\开源data\教育.xlsx')
# 转换标签
updata_label('整体数据.xlsx')