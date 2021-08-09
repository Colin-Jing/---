import pandas as pd
from tqdm import tqdm

def data_process():
    # 创建一个空的 DataFrame
    train_df = pd.DataFrame(columns=['content', 'channelName'])
    test_df = pd.DataFrame(columns=['content', 'channelName'])
    # 导入数据
    for i in range(10):
        df = pd.read_excel(r'C:\Users\Colin_Jing\竞赛\中国软件杯\1617241934831197.xlsx',sheet_name=i)
    # 生成训练集
        #生成新的DataFrame，不要索引
        #print(df.columns.tolist())
        #print(df.shape[0])
        content_train_df = df.loc[0:(df.shape[0]-int(df.shape[0]/10)),['content','channelName']]
        title_train_df = df.loc[0:(df.shape[0]-int(df.shape[0]/10)),['title','channelName']]
        content_test_df = df.loc[(df.shape[0]-int(df.shape[0]/10)+1):df.shape[0],['content','channelName']]
        title_train_df = df.loc[(df.shape[0]-int(df.shape[0]/10)+1):df.shape[0],['title','channelName']]
        if i > 0:
            train_df = pd.concat([train_df,content_train_df],axis=0,join='outer',ignore_index=True)
            test_df = pd.concat([test_df,content_test_df],axis=0,join='outer',ignore_index=True)
        else:
            train_df = content_train_df
    #print(train_df.shape)
    train_df.to_excel(r'./data/train.xlsx',index=False)
    # 生成测试集
    test_df.to_excel(r'./data/test.xlsx',index=False)

def data_process_more():
    tmp_file = pd.read_excel(r'./data/train.xlsx')
    #
    for i in range(len(tmp_file['channelName'])):
        if tmp_file['channelName'][i] == '综合体育最新':
           tmp_file['channelName'][i] = '体育'
        elif tmp_file['channelName'][i] == '体育焦点':
            tmp_file['channelName'][i] = '娱乐'
    tmp_file.to_excel(r'./data/train.xlsx',index=False)

    tmp_file = pd.read_excel(r'./data/test.xlsx')
    #
    for i in range(len(tmp_file['channelName'])):
        if tmp_file['channelName'][i] == '综合体育最新':
           tmp_file['channelName'][i] = '体育'
        elif tmp_file['channelName'][i] == '体育焦点':
            tmp_file['channelName'][i] = '娱乐'
    tmp_file.to_excel(r'./data/test.xlsx',index=False)
#  先这样分着， 但我觉得数据量差距太大了，可能我还需要爬虫去爬一些数据，使各类别的数据数量大致相等
def label_transform():
    label_list = ['财经','房产','教育','科技','军事','汽车','体育','游戏','娱乐']
    tmp_file = pd.read_excel(r'./data/train.xlsx')
    #
    for k in range(len(label_list)):
        for i in range(len(tmp_file['channelName'])):
            if tmp_file['channelName'][i] == label_list[k]:
                tmp_file['channelName'][i] = k
    tmp_file.to_excel(r'./data/train.xlsx', index=False)

    tmp_file = pd.read_excel(r'./data/test.xlsx')
    #
    for k in range(len(label_list)):
        for i in range(len(tmp_file['channelName'])):
            if tmp_file['channelName'][i] == label_list[k]:
                tmp_file['channelName'][i] = k
    tmp_file.to_excel(r'./data/test.xlsx', index=False)

def xlsx_to_txt():
    tmp_file = pd.read_excel(r'./data/train.xlsx')
    with open(r'./THUCNews/data/train.txt', 'w', encoding='UTF-8') as f:
        for i in range(tmp_file.shape[0]):
            text_1 = str(tmp_file.loc[i, ['content']].values[0])[0:50]
            text_1 = text_1.replace('\n', '')
            text_1 = text_1.replace('\r', '')
            text_1 = text_1.replace('\t','')
            text_1 = text_1.replace(' ','')
            text_2 = str(tmp_file.loc[i, ['channelName']].values[0])
            f.write(text_1 + '\t' + text_2 + '\n')
    print('train finished!!!')
    tmp_file = pd.read_excel(r'./data/test.xlsx')
    with open(r'./THUCNews/data/test.txt', 'w', encoding='UTF-8') as f:
        for i in range(tmp_file.shape[0]):
            text_1 = str(tmp_file.loc[i, ['content']].values[0])[0:50]
            text_1 = text_1.replace('\n', '')
            text_1 = text_1.replace('\r', '')
            text_1 = text_1.replace('\t', '')
            text_1 = text_1.replace(' ', '')
            text_2 = str(tmp_file.loc[i, ['channelName']].values[0])
            f.write(text_1 + '\t' + text_2 + '\n')
    print('test finished!!!')

    tmp_file = pd.read_excel(r'./THUCNews/data/dev.xlsx')
    with open(r'./THUCNews/data/dev.txt', 'w', encoding='UTF-8') as f:
        for i in range(tmp_file.shape[0]):
            text_1 = str(tmp_file.loc[i, ['content']].values[0])[0:50]
            text_1 = text_1.replace('\n', '')
            text_1 = text_1.replace('\r', '')
            text_1 = text_1.replace('\t', '')
            text_1 = text_1.replace(' ', '')
            text_2 = str(tmp_file.loc[i, ['channelName']].values[0])
            f.write(text_1 + '\t' + text_2 + '\n')
    print('dev finished!!!')
#xlsx_to_txt()

def txt_to_xlsx():
    with open(r'C:\Users\Colin_Jing\竞赛\中国软件杯\text\THUCNews\data\dev.txt', 'r', encoding='UTF-8') as f:
        with open(r'./data/dev.xlsx','a',encoding='UTF-8') as file:
            for line in tqdm(f):
                lin = line.strip()
                if not lin:
                    continue
                content, label = lin.split('\t')
                if label == 2:
                    label = 0
                elif label == 3:
                    label = 2
                elif label == 4:
                    label = 3
                elif label == 5:
                    label = 9
                elif label == 6:
                    label = 4
                elif label == 7:
                    label = 6
                elif label == 8:
                    label = 7
                elif label == 9:
                    label = 8
                file.write(content+'\t'+label+'\n')
