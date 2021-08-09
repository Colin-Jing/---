import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow,QFileDialog
from mainForm import Ui_MainWindow
import time
from for_detect import detect
from importlib import import_module
import argparse
from utils import build_iterator
from for_detect import build_dataset
import torch

parser = argparse.ArgumentParser(description='Chinese Text Classification')
parser.add_argument('--word', default=False, type=bool, help='True for word, False for char')
args = parser.parse_args()
dataset = 'THUCNews'  # 数据集

# 搜狗新闻:embedding_SougouNews.npz, 腾讯:embedding_Tencent.npz, 随机初始化:random（词嵌入模型，即每个词对应的向量）
embedding = 'embedding_SougouNews.npz'
model_name = 'TextDetect'  # TextCNN, TextRNN,

x = import_module('models.' + model_name)
config = x.Config(dataset, embedding)

# detect

model = x.Model(config).to(config.device)
print("load weight")
model.load_state_dict(torch.load(config.save_path))
model.eval()
print("load finished")

def model_test():
    vocab, test_data = build_dataset(config, args.word)  # 数据读取
    test_iter = build_iterator(test_data, config)
    config.n_vocab = len(vocab)
    # 检测
    result = detect(config, model, test_iter)
    print(result)
    return result

class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.n = 1
        self.textEdit1Input.setText("") # 单条输入
        self.textEdit.setText("") # 单条识别结果
        self.lineEdit1TimeResult.setText("") # 单条时间
        self.lineEdit2Result.setText("") # 批量结果路径
        self.lineEdit2Time.setText("")  # 批量时间
        self.lineEdit_4.setText("")  # 批量excel文件输入路径
        self.label2Result.setText("识别结果:")
        self.pushButton1Start.clicked.connect(self.detect_new)
        self.pushButton2Open.clicked.connect(self.choose_ecxel)
        self.pushButton2Start.clicked.connect(self.detect_excel)


    def detect_new(self):
        self.str1 = self.textEdit1Input.toPlainText()
        config.test_path = str(self.str1)
        print(config.test_path)
        start = time.time()
        result_word = model_test()
        end = time.time()
        self.textEdit.setText(result_word)
        self.lineEdit1TimeResult.setText(str(end-start))


    def choose_ecxel(self):
        try:
            self.excel_path = QFileDialog.getOpenFileName(self, "选取excel文件", r".","Text Files (*.xlsx)")
        except:
            pass
        config.test_path = self.excel_path[0]
        path_name = os.path.split(config.test_path)[1].split(".")[0]
        config.result_path = config.result_path.format(path_name)
        self.lineEdit_4.setText(config.test_path)



    def detect_excel(self):
        print("开始识别")
        start = time.time()
        result_word = model_test()
        QtWidgets.QApplication.processEvents()
        end = time.time()
        print("识别完成")
        path = os.getcwd().replace("\\","/")
        self.lineEdit2Result.setText(path + "/" + result_word)
        self.lineEdit2Time.setText(str(end - start))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())


