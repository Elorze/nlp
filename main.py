import sys
import os
import logging
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QTextEdit, QLabel, QHBoxLayout, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QTextCursor
from src.poem_classifier import PoemClassifier
from src.generate_poem import generate_poem
from src.poem_scorer import PoemScorer
from src.emotion_analyzer import EmotionAnalyzer
from src.poem_annotator import PoemAnnotator
from src.poem_translator import PoemTranslator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class PoemAnalysisSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # 初始化分类器
        self.classifier = PoemClassifier()
        try:
            self.classifier.train()
        except Exception as e:
            QMessageBox.warning(self, "警告", f"分类器初始化失败：{str(e)}")
        
        # 初始化评分器
        self.scorer = PoemScorer()
        
        # 初始化情感分析器
        self.emotion_analyzer = EmotionAnalyzer()
        
        # 初始化注释器
        self.annotator = PoemAnnotator()
        
        # 初始化翻译器
        self.translator = PoemTranslator()
        
        # 示例诗词库（包含诗词和正确的标签）
        self.example_poems = [
            ("春眠不觉晓处处闻啼鸟夜来风雨声花落知多少", "山水"),
            ("床前明月光疑是地上霜举头望明月低头思故乡", "山水"),
            ("白日依山尽黄河入海流欲穷千里目更上一层楼", "山水"),
            ("千山鸟飞绝万径人踪灭孤舟蓑笠翁独钓寒江雪", "山水"),
            ("两个黄鹂鸣翠柳一行白鹭上青天窗含西岭千秋雪门泊东吴万里船", "山水"),
            ("秦时明月汉时关万里长征人未还但使龙城飞将在不教胡马度阴山", "咏史"),
            ("朱雀桥边野草花乌衣巷口夕阳斜旧时王谢堂前燕飞入寻常百姓家", "咏史"),
            ("折戟沉沙铁未销自将磨洗认前朝东风不与周郎便铜雀春深锁二乔", "咏史"),
            ("烟笼寒水月笼沙夜泊秦淮近酒家商女不知亡国恨隔江犹唱后庭花", "咏史"),
            ("胜败兵家事不期包羞忍耻是男儿江东子弟多才俊卷土重来未可知", "咏史"),
            ("渭城朝雨浥轻尘客舍青青柳色新劝君更尽一杯酒西出阳关无故人", "送别"),
            ("故人西辞黄鹤楼烟花三月下扬州孤帆远影碧空尽唯见长江天际流", "送别"),
            ("寒雨连江夜入吴平明送客楚山孤洛阳亲友如相问一片冰心在玉壶", "送别"),
            ("城阙辅三秦风烟望五津与君离别意同是宦游人海内存知己天涯若比邻", "送别"),
            ("千里黄云白日曛北风吹雁雪纷纷莫愁前路无知己天下谁人不识君", "送别")
        ]

    def initUI(self):
        self.setWindowTitle('诗词分析系统')
        self.setGeometry(100, 100, 1200, 800)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建按钮布局
        button_layout = QHBoxLayout()

        # 创建按钮
        btn_classify = QPushButton('诗词分类', self)
        btn_generate = QPushButton('诗词生成与评分', self)
        btn_emotion = QPushButton('诗词情感分析', self)
        btn_annotate = QPushButton('关键词高亮与注释', self)
        btn_translate = QPushButton('古今对照解释', self)

        # 添加按钮到布局
        button_layout.addWidget(btn_classify)
        button_layout.addWidget(btn_generate)
        button_layout.addWidget(btn_emotion)
        button_layout.addWidget(btn_annotate)
        button_layout.addWidget(btn_translate)

        # 创建结果显示区域
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont('SimSun', 12))

        # 添加部件到布局
        layout.addLayout(button_layout)
        layout.addWidget(self.result_text)

        # 连接信号
        btn_classify.clicked.connect(self.classify_poems)
        btn_generate.clicked.connect(self.generate_and_score_poems)
        btn_emotion.clicked.connect(self.analyze_emotions)
        btn_annotate.clicked.connect(self.annotate_poems)
        btn_translate.clicked.connect(self.translate_poem)

    def classify_poems(self):
        try:
            # 随机选择5首诗
            selected_poems = random.sample(self.example_poems, 5)
            
            # 清空结果显示区域
            self.result_text.clear()
            
            # 统计正确分类的数量
            correct_count = 0
            
            # 对每首诗进行分类
            for poem, true_label in selected_poems:
                result = self.classifier.predict(poem)
                if result:
                    predicted_label = result['label']
                    is_correct = predicted_label == true_label
                    if is_correct:
                        correct_count += 1
                    
                    # 构建显示文本
                    display_text = f"诗词：{poem}\n"
                    display_text += f"预测类别：{predicted_label}\n"
                    display_text += f"正确类别：{true_label}\n"
                    display_text += f"分类{'正确' if is_correct else '错误'}\n"
                    display_text += "\n" + "-"*50 + "\n\n"
                    
                    # 显示结果
                    self.result_text.append(display_text)
                else:
                    self.result_text.append(f"诗词分类失败：{poem}\n\n")
            
            # 显示总体准确率
            accuracy = correct_count / 5 * 100
            self.result_text.append(f"\n总体准确率：{accuracy:.1f}%")
                    
        except Exception as e:
            QMessageBox.warning(self, "错误", f"分类过程出现错误：{str(e)}")

    def generate_and_score_poems(self):
        try:
            # 清空结果显示区域
            self.result_text.clear()
            
            # 生成5首诗词并评分
            result_text = "生成的五首诗词及评分：\n\n"
            for i in range(5):
                try:
                    # 生成诗词
                    poem = generate_poem()
                    # 评分
                    result = self.scorer.score_poem(poem)
                    
                    # 构建显示文本
                    result_text += f"第{i+1}首：\n{poem}\n\n"
                    result_text += "评分结果：\n"
                    for metric, score in result['scores'].items():
                        result_text += f"{metric}: {score:.1f}分\n"
                    result_text += f"总分：{result['total_score']:.1f}分\n"
                    result_text += f"分析：\n"
                    for aspect, analysis in result['analysis'].items():
                        result_text += f"{aspect}：{analysis}\n"
                    result_text += "\n" + "="*50 + "\n\n"
                except Exception as e:
                    result_text += f"第{i+1}首生成失败：{str(e)}\n\n"
                    continue
            
            # 显示结果
            self.result_text.setText(result_text)
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成诗词时出现错误：{str(e)}")

    def analyze_emotions(self):
        try:
            # 清空结果显示区域
            self.result_text.clear()
            
            # 随机选择5首诗进行情感分析
            selected_poems = random.sample(self.example_poems, 5)
            
            result_text = "诗词情感分析结果：\n\n"
            for i, (poem, _) in enumerate(selected_poems, 1):
                try:
                    # 进行情感分析
                    result = self.emotion_analyzer.analyze_emotion(poem)
                    
                    # 构建显示文本
                    result_text += f"第{i}首：\n{poem}\n\n"
                    result_text += "情感分析结果：\n"
                    result_text += f"主要情感：{result['main_emotion']}\n"
                    if result['secondary_emotion']:
                        result_text += f"辅助情感：{result['secondary_emotion']}\n"
                    
                    # 显示意象分析
                    if result['imagery_emotions']:
                        result_text += "\n意象分析：\n"
                        for imagery, emotion in result['imagery_emotions']:
                            result_text += f"「{imagery}」（{emotion}）\n"
                    
                    # 显示情感分布
                    result_text += "\n情感分布：\n"
                    sorted_scores = sorted(result['emotion_scores'].items(), key=lambda x: x[1], reverse=True)[:2]
                    for emotion, score in sorted_scores:
                        result_text += f"{emotion}: {score:.2f}\n"
                    
                    result_text += "\n" + "="*50 + "\n\n"
                except Exception as e:
                    result_text += f"第{i}首分析失败：{str(e)}\n\n"
                    continue
            
            # 显示结果
            self.result_text.setText(result_text)
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"情感分析过程出现错误：{str(e)}")

    def annotate_poems(self):
        """诗词关键词高亮与注释"""
        self.result_text.clear()
        self.result_text.setHtml("<h2 style='color: #333;'>诗词关键词高亮与注释</h2>")
        
        # 生成5首诗词
        for i in range(5):
            try:
                # 生成诗词
                poem = generate_poem()
                if not poem:
                    continue
                    
                # 高亮关键词并获取注释
                highlighted_poem, annotations = self.annotator.highlight_and_annotate(poem)
                
                # 显示诗词
                self.result_text.append(f"<h3 style='color: #666;'>诗词 {i+1}：</h3>")
                self.result_text.append(f"<p style='font-size: 16px; line-height: 1.8;'>{highlighted_poem}</p>")
                
                # 显示注释
                if annotations:
                    self.result_text.append("<div style='margin: 10px 0; padding: 10px; background-color: #f5f5f5; border-radius: 5px;'>")
                    self.result_text.append("<h4 style='color: #666; margin: 0 0 10px 0;'>关键词注释：</h4>")
                    for anno in annotations:
                        self.result_text.append(f"<p style='margin: 5px 0;'>{anno}</p>")
                    self.result_text.append("</div>")
                else:
                    self.result_text.append("<p style='color: #999;'>暂无关键词高亮</p>")
                
                self.result_text.append("<hr style='border: 1px solid #eee; margin: 20px 0;'>")
                
            except Exception as e:
                self.result_text.append(f"<p style='color: red;'>处理诗词时出错：{str(e)}</p>")
                continue

    def translate_poem(self):
        """古今对照解释功能"""
        try:
            # 清空结果区域
            self.result_text.clear()
            
            # 获取随机诗词
            poem = self.translator.get_random_poem()
            
            # 翻译诗词
            result = self.translator.translate_poem(poem)
            
            # 显示结果
            html = f"""
            <div style='margin: 20px;'>
                <h2 style='color: #2c3e50;'>古今对照解释</h2>
                <div style='margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px;'>
                    <h3 style='color: #34495e;'>原文：</h3>
                    <p style='font-size: 16px; color: #2c3e50;'>{result['original']}</p>
                </div>
                <div style='margin: 20px 0; padding: 15px; background-color: #e8f4f8; border-radius: 5px;'>
                    <h3 style='color: #34495e;'>直译：</h3>
                    <p style='font-size: 16px; color: #2c3e50;'>{result['translation']}</p>
                </div>
            </div>
            """
            self.result_text.setHtml(html)
            
        except Exception as e:
            logging.error(f"翻译诗词时出错：{str(e)}")
            self.result_text.setHtml(f"<p style='color: red;'>处理出错：{str(e)}</p>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PoemAnalysisSystem()
    ex.show()
    sys.exit(app.exec_()) 