import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                            QTabWidget, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import random
import logging
from test_classifier import classify_poem
from poem_scorer import PoemScorer
from generate_poem import generate_poem
from poem_classifier import PoemClassifier
from emotion_analyzer import EmotionAnalyzer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class PoetryAnalysisUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.poem_scorer = PoemScorer()
        self.init_ui()
        self.load_example_poems()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('诗词分析系统')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # 创建标签页
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # 创建三个标签页
        self.classify_tab = QWidget()
        self.generate_tab = QWidget()
        self.score_tab = QWidget()
        
        tabs.addTab(self.classify_tab, "诗词分类")
        tabs.addTab(self.generate_tab, "诗词生成")
        tabs.addTab(self.score_tab, "诗词评分")
        
        # 初始化各个标签页
        self.init_classify_tab()
        self.init_generate_tab()
        self.init_score_tab()
        
    def init_classify_tab(self):
        """初始化分类标签页"""
        layout = QVBoxLayout()
        
        # 输入区域
        input_label = QLabel("请输入要分类的诗词：")
        self.classify_input = QTextEdit()
        self.classify_input.setPlaceholderText("在此输入诗词...")
        self.classify_input.setMinimumHeight(100)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        classify_btn = QPushButton("开始分类")
        classify_btn.clicked.connect(self.on_classify)
        random_btn = QPushButton("随机选择诗词")
        random_btn.clicked.connect(self.on_random_select)
        button_layout.addWidget(classify_btn)
        button_layout.addWidget(random_btn)
        
        # 输出区域
        output_label = QLabel("分类结果：")
        self.classify_output = QTextEdit()
        self.classify_output.setReadOnly(True)
        
        # 添加所有组件到布局
        layout.addWidget(input_label)
        layout.addWidget(self.classify_input)
        layout.addLayout(button_layout)
        layout.addWidget(output_label)
        layout.addWidget(self.classify_output)
        
        self.classify_tab.setLayout(layout)
        
    def init_generate_tab(self):
        """初始化生成标签页"""
        layout = QVBoxLayout()
        
        # 输出区域
        output_label = QLabel("生成的诗词：")
        self.generate_output = QTextEdit()
        self.generate_output.setReadOnly(True)
        
        # 按钮
        generate_btn = QPushButton("生成五首诗词")
        generate_btn.clicked.connect(self.on_generate_five)
        
        # 添加组件到布局
        layout.addWidget(output_label)
        layout.addWidget(self.generate_output)
        layout.addWidget(generate_btn)
        
        self.generate_tab.setLayout(layout)
        
    def init_score_tab(self):
        """初始化评分标签页"""
        layout = QVBoxLayout()
        
        # 输入区域
        input_label = QLabel("请输入要评分的诗词：")
        self.score_input = QTextEdit()
        self.score_input.setPlaceholderText("在此输入诗词...")
        self.score_input.setMinimumHeight(100)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        score_btn = QPushButton("开始评分")
        score_btn.clicked.connect(self.on_score)
        random_btn = QPushButton("随机选择诗词")
        random_btn.clicked.connect(self.on_random_select_score)
        button_layout.addWidget(score_btn)
        button_layout.addWidget(random_btn)
        
        # 输出区域
        output_label = QLabel("评分结果：")
        self.score_output = QTextEdit()
        self.score_output.setReadOnly(True)
        
        # 添加所有组件到布局
        layout.addWidget(input_label)
        layout.addWidget(self.score_input)
        layout.addLayout(button_layout)
        layout.addWidget(output_label)
        layout.addWidget(self.score_output)
        
        self.score_tab.setLayout(layout)
        
    def load_example_poems(self):
        """加载示例诗词"""
        try:
            self.example_poems = pd.read_csv('data/example_poems.csv')
            logging.info("成功加载示例诗词")
        except Exception as e:
            logging.error(f"加载示例诗词失败：{str(e)}")
            self.example_poems = pd.DataFrame({
                'content': [
                    "春眠不觉晓处处闻啼鸟夜来风雨声花落知多少",
                    "床前明月光疑是地上霜举头望明月低头思故乡",
                    "白日依山尽黄河入海流欲穷千里目更上一层楼",
                    "千山鸟飞绝万径人踪灭孤舟蓑笠翁独钓寒江雪",
                    "两个黄鹂鸣翠柳一行白鹭上青天窗含西岭千秋雪门泊东吴万里船"
                ],
                'label': [0, 0, 1, 0, 1]
            })
    
    def on_classify(self):
        """处理分类按钮点击事件"""
        try:
            poem = self.classify_input.toPlainText().strip()
            if not poem:
                QMessageBox.warning(self, "警告", "请输入要分类的诗词！")
                return
                
            category, report = classify_poem(poem)
            self.classify_output.setText(report)
            logging.info(f"成功分类诗词：{poem}")
        except Exception as e:
            error_msg = f"分类失败：{str(e)}"
            self.classify_output.setText(error_msg)
            logging.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def on_generate_five(self):
        """处理生成五首诗词按钮点击事件"""
        try:
            result_text = "生成的五首诗词及评分：\n\n"
            for i in range(5):
                # 生成诗词
                poem = generate_poem()
                # 评分
                result = self.poem_scorer.score_poem(poem)
                total_score = result['total_score']
                scores = result['scores']
                analysis = result['analysis']
                # 添加到结果文本
                result_text += f"第{i+1}首：\n{poem}\n\n总分：{total_score:.2f}\n"
                for key, value in scores.items():
                    result_text += f"{key}: {value:.2f}\n"
                result_text += "分析：\n"
                for key, value in analysis.items():
                    result_text += f"{key}: {value}\n"
                result_text += f"{'='*50}\n\n"
            self.generate_output.setText(result_text)
            logging.info("成功生成五首诗词并评分")
        except Exception as e:
            error_msg = f"生成失败：{str(e)}"
            self.generate_output.setText(error_msg)
            logging.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def on_score(self):
        """处理评分按钮点击事件"""
        try:
            poem = self.score_input.toPlainText().strip()
            if not poem:
                QMessageBox.warning(self, "警告", "请输入要评分的诗词！")
                return
            result = self.poem_scorer.score_poem(poem)
            total_score = result['total_score']
            scores = result['scores']
            analysis = result['analysis']
            report = f"总分：{total_score:.2f}\n"
            for key, value in scores.items():
                report += f"{key}: {value:.2f}\n"
            report += "分析：\n"
            for key, value in analysis.items():
                report += f"{key}: {value}\n"
            self.score_output.setText(report)
            logging.info(f"成功评分诗词：{poem}")
        except Exception as e:
            error_msg = f"评分失败：{str(e)}"
            self.score_output.setText(error_msg)
            logging.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def on_random_select(self):
        """随机选择诗词进行分类"""
        try:
            if len(self.example_poems) > 0:
                poem = random.choice(self.example_poems['content'].tolist())
                self.classify_input.setText(poem)
                self.on_classify()
                logging.info(f"随机选择诗词：{poem}")
            else:
                QMessageBox.warning(self, "警告", "没有可用的示例诗词！")
        except Exception as e:
            error_msg = f"随机选择失败：{str(e)}"
            logging.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def on_random_select_score(self):
        """随机选择诗词进行评分"""
        try:
            if len(self.example_poems) > 0:
                poem = random.choice(self.example_poems['content'].tolist())
                self.score_input.setText(poem)
                self.on_score()
                logging.info(f"随机选择诗词：{poem}")
            else:
                QMessageBox.warning(self, "警告", "没有可用的示例诗词！")
        except Exception as e:
            error_msg = f"随机选择失败：{str(e)}"
            logging.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)

def main():
    try:
        app = QApplication(sys.argv)
        
        # 设置应用程序样式
        app.setStyle('Fusion')
        
        # 设置字体
        font = QFont("Microsoft YaHei", 10)
        app.setFont(font)
        
        window = PoetryAnalysisUI()
        window.show()
        
        logging.info("应用程序启动成功")
        sys.exit(app.exec_())
    except Exception as e:
        logging.critical(f"应用程序启动失败：{str(e)}")
        QMessageBox.critical(None, "错误", f"应用程序启动失败：{str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 