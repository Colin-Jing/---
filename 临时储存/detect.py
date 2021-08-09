import time
from for_detect import detect
from importlib import import_module
import argparse
from utils import build_iterator, get_time_dif
from for_detect import build_dataset
import torch

parser = argparse.ArgumentParser(description='Chinese Text Classification')
parser.add_argument('--model', default='TextDetect',type=str, required=True, help='choose a model: TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer')
parser.add_argument('--embedding', default='pre_trained', type=str, help='random or pre_trained')
parser.add_argument('--word', default=False, type=bool, help='True for word, False for char')
args = parser.parse_args()
dataset = 'THUCNews'  # 数据集

# 搜狗新闻:embedding_SougouNews.npz, 腾讯:embedding_Tencent.npz, 随机初始化:random（词嵌入模型，即每个词对应的向量）
embedding = 'embedding_SougouNews.npz'
if args.embedding == 'random':
    embedding = 'random'
model_name = args.model  # TextCNN, TextRNN,

x = import_module('models.' + model_name)
config = x.Config(dataset, embedding)
start_time = time.time()
print("Loading data...")
vocab, test_data = build_dataset(config, args.word)  # 数据读取
test_iter = build_iterator(test_data, config)
time_dif = get_time_dif(start_time)
print("Time usage:", time_dif)  # 计算拿到batch的时间

# detect
config.n_vocab = len(vocab)
model = x.Model(config).to(config.device)
print("load weight")
model.load_state_dict(torch.load(config.save_path))
model.eval()
print("load finished")


def mian():
    # 检测
    result = detect(config, model, test_iter)
    print(result)

if __name__ == '__main__':
    mian()

