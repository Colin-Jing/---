from PyQt5.QtGui import QPixmap,QIcon
import sys
import os
from PyQt5.QtWidgets import QMainWindow,QApplication,QGraphicsPixmapItem,QGraphicsScene,QGraphicsItem,QFileDialog,QMessageBox
from PyQt5.QtCore import QStringListModel
from MianWin import Ui_MainWindow
import time
from for_detect import detect
from importlib import import_module
import argparse
from utils import build_iterator, get_time_dif
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


class MyQWidget(QMainWindow):#,Ui_MainWindow
    def __init__(self,parent=None):
        super(MyQWidget,self).__init__(parent)
        self.UI()
        self.ui.textEdit.setText("在此输入单条新闻")
        self.ui.textEdit_2.setText("")
        self.ui.label_6.setText("暂无识别")
        self.ui.pushButton.clicked.connect(self.getword)
        self.ui.pushButton_2.clicked.connect(self.getexcelfile)
    def UI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

    # 获取单条文本的内容
    def getword(self):
        self.str1 = self.ui.textEdit.toPlainText()
        config.test_path = str(self.str1)
        print(config.test_path)
        self.detectnew()

    #识别单条文本的内容并打印
    def detectnew(self):
        result_word = model_test()
        self.ui.textEdit_2.setText(result_word)

    def getexcelfile(self):
        self.ui.label_6.setText("识别中")
        try:
            self.excel_path = QFileDialog.getOpenFileName(self, "选取excel文件", r".","Text Files (*.xlsx)")
        except:
            pass
        print(self.excel_path[0])
        config.test_path = self.excel_path[0]
        print(config.test_path)
        self.detectnews()
    def detectnews(self):
        print("开始识别")
        result_word = model_test()
        print("识别完成")
        self.ui.label_6.setText("识别结束！！！")
        self.ui.label_5.setText(str(config.result_path))


def main():
    app = QApplication(sys.argv)
    w = MyQWidget()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()