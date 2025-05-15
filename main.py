import sys
import os
import logging
import random
import urllib.request
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QTextEdit, QLabel, QHBoxLayout, QMessageBox, QFileDialog,
                           QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QTextCursor, QPalette, QIcon, QPixmap, QBrush, QLinearGradient
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
        
        # 检查并下载竹子水墨画图片
        bg_path = "resources/bamboo_bg.jpg"
        bg_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"
        if not os.path.exists(bg_path):
            os.makedirs("resources", exist_ok=True)
            urllib.request.urlretrieve(bg_url, bg_path)
        
        # 设置窗口背景为竹子水墨画
        palette = QPalette()
        pixmap = QPixmap(bg_path)
        scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 创建标题
        title_label = QLabel('诗词分析系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont('SimSun', 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet('color: #8B4513; margin-bottom: 20px; background: rgba(255,255,255,0.7); border-radius: 8px;')
        layout.addWidget(title_label)

        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # 创建按钮样式
        button_style = """
            QPushButton {
                background-color: rgba(245,222,179,0.85);
                border: 2px solid #8B4513;
                border-radius: 10px;
                padding: 10px 20px;
                color: #8B4513;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DEB887;
                border-color: #654321;
            }
            QPushButton:pressed {
                background-color: #D2691E;
                color: white;
            }
        """

        # 创建按钮
        btn_classify = QPushButton('诗词分类', self)
        btn_generate = QPushButton('诗词生成与评分', self)
        btn_emotion = QPushButton('诗词情感分析', self)
        btn_annotate = QPushButton('关键词高亮与注释', self)
        btn_translate = QPushButton('古今对照解释', self)

        # 设置按钮样式
        for btn in [btn_classify, btn_generate, btn_emotion, btn_annotate, btn_translate]:
            btn.setStyleSheet(button_style)
            btn.setMinimumHeight(40)
            button_layout.addWidget(btn)

        # 创建结果显示区域
        result_frame = QFrame()
        result_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        result_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(250,240,230,0.85);
                border: 2px solid #8B4513;
                border-radius: 15px;
            }
        """)
        
        result_layout = QVBoxLayout(result_frame)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5DEB3;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #8B4513;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont('SimSun', 12))
        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(250,240,230,0.7);
                border: none;
                color: #4A4A4A;
                padding: 15px;
            }
        """)
        
        scroll_area.setWidget(self.result_text)
        result_layout.addWidget(scroll_area)

        # 添加部件到布局
        layout.addLayout(button_layout)
        layout.addWidget(result_frame)

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
            
            # 添加标题
            self.result_text.append('<h2 style="color: #8B4513; text-align: center;">诗词分类结果</h2>')
            
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
                    display_text = f'<div style="margin: 15px; padding: 15px; background-color: #FFF8DC; border-radius: 10px;">'
                    display_text += f'<p style="font-size: 16px; color: #8B4513;"><b>诗词：</b>{poem}</p>'
                    display_text += f'<p style="font-size: 14px;"><b>预测类别：</b><span style="color: {"#228B22" if is_correct else "#B22222"}">{predicted_label}</span></p>'
                    display_text += f'<p style="font-size: 14px;"><b>正确类别：</b>{true_label}</p>'
                    display_text += f'<p style="font-size: 14px; color: {"#228B22" if is_correct else "#B22222"}"><b>分类{"正确" if is_correct else "错误"}</b></p>'
                    display_text += '</div>'
                    
                    # 显示结果
                    self.result_text.append(display_text)
                else:
                    self.result_text.append(f'<div style="color: #B22222;">诗词分类失败：{poem}</div>')
            
            # 显示总体准确率
            accuracy = correct_count / 5 * 100
            self.result_text.append(f'<div style="text-align: center; margin-top: 20px; font-size: 16px; color: #8B4513;"><b>总体准确率：{accuracy:.1f}%</b></div>')
                    
        except Exception as e:
            QMessageBox.warning(self, "错误", f"分类过程出现错误：{str(e)}")

    def generate_and_score_poems(self):
        try:
            # 清空结果显示区域
            self.result_text.clear()
            
            # 添加标题
            self.result_text.append('<h2 style="color: #8B4513; text-align: center;">生成的诗词及评分</h2>')
            
            # 生成5首诗词并评分
            for i in range(5):
                try:
                    # 生成诗词
                    poem = generate_poem()
                    # 评分
                    result = self.scorer.score_poem(poem)
                    
                    # 构建显示文本
                    display_text = f'<div style="margin: 15px; padding: 15px; background-color: #FFF8DC; border-radius: 10px;">'
                    display_text += f'<h3 style="color: #8B4513;">第{i+1}首：</h3>'
                    display_text += f'<p style="font-size: 16px; line-height: 1.8;">{poem}</p>'
                    display_text += '<div style="margin-top: 10px;">'
                    display_text += '<h4 style="color: #8B4513;">评分结果：</h4>'
                    for metric, score in result['scores'].items():
                        display_text += f'<p style="margin: 5px 0;"><b>{metric}:</b> {score:.1f}分</p>'
                    display_text += f'<p style="margin: 5px 0;"><b>总分：</b>{result["total_score"]:.1f}分</p>'
                    display_text += '</div>'
                    display_text += '<div style="margin-top: 10px;">'
                    display_text += '<h4 style="color: #8B4513;">分析：</h4>'
                    for aspect, analysis in result['analysis'].items():
                        display_text += f'<p style="margin: 5px 0;"><b>{aspect}：</b>{analysis}</p>'
                    display_text += '</div>'
                    display_text += '</div>'
                    
                    # 显示结果
                    self.result_text.append(display_text)
                except Exception as e:
                    self.result_text.append(f'<div style="color: #B22222;">第{i+1}首生成失败：{str(e)}</div>')
                    continue
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成诗词时出现错误：{str(e)}")

    def analyze_emotions(self):
        try:
            # 清空结果显示区域
            self.result_text.clear()
            
            # 添加标题
            self.result_text.append('<h2 style="color: #8B4513; text-align: center;">诗词情感分析结果</h2>')
            
            # 随机选择5首诗进行情感分析
            selected_poems = random.sample(self.example_poems, 5)
            
            for i, (poem, _) in enumerate(selected_poems, 1):
                try:
                    # 进行情感分析
                    result = self.emotion_analyzer.analyze_emotion(poem)
                    
                    # 构建显示文本
                    display_text = f'<div style="margin: 15px; padding: 15px; background-color: #FFF8DC; border-radius: 10px;">'
                    display_text += f'<h3 style="color: #8B4513;">第{i}首：</h3>'
                    display_text += f'<p style="font-size: 16px; line-height: 1.8;">{poem}</p>'
                    display_text += '<div style="margin-top: 10px;">'
                    display_text += '<h4 style="color: #8B4513;">情感分析结果：</h4>'
                    display_text += f'<p style="margin: 5px 0;"><b>主要情感：</b>{result["main_emotion"]}</p>'
                    if result['secondary_emotion']:
                        display_text += f'<p style="margin: 5px 0;"><b>辅助情感：</b>{result["secondary_emotion"]}</p>'
                    
                    # 显示意象分析
                    if result['imagery_emotions']:
                        display_text += '<div style="margin-top: 10px;">'
                        display_text += '<h4 style="color: #8B4513;">意象分析：</h4>'
                        for imagery, emotion in result['imagery_emotions']:
                            display_text += f'<p style="margin: 5px 0;">「{imagery}」（{emotion}）</p>'
                        display_text += '</div>'
                    
                    # 显示情感分布
                    display_text += '<div style="margin-top: 10px;">'
                    display_text += '<h4 style="color: #8B4513;">情感分布：</h4>'
                    sorted_scores = sorted(result['emotion_scores'].items(), key=lambda x: x[1], reverse=True)[:2]
                    for emotion, score in sorted_scores:
                        display_text += f'<p style="margin: 5px 0;"><b>{emotion}:</b> {score:.2f}</p>'
                    display_text += '</div>'
                    display_text += '</div>'
                    display_text += '</div>'
                    
                    # 显示结果
                    self.result_text.append(display_text)
                except Exception as e:
                    self.result_text.append(f'<div style="color: #B22222;">第{i}首分析失败：{str(e)}</div>')
                    continue
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"情感分析过程出现错误：{str(e)}")

    def annotate_poems(self):
        """诗词关键词高亮与注释"""
        self.result_text.clear()
        self.result_text.append('<h2 style="color: #8B4513; text-align: center;">诗词关键词高亮与注释</h2>')
        
        # 生成5首诗词
        for i in range(5):
            try:
                # 生成诗词
                poem = generate_poem()
                if not poem:
                    continue
                    
                # 高亮关键词并获取注释
                highlighted_poem, annotations = self.annotator.highlight_and_annotate(poem)
                
                # 构建显示文本
                display_text = f'<div style="margin: 15px; padding: 15px; background-color: #FFF8DC; border-radius: 10px;">'
                display_text += f'<h3 style="color: #8B4513;">诗词 {i+1}：</h3>'
                display_text += f'<p style="font-size: 16px; line-height: 1.8;">{highlighted_poem}</p>'
                
                # 显示注释
                if annotations:
                    display_text += '<div style="margin-top: 10px; padding: 10px; background-color: #FAF0E6; border-radius: 5px;">'
                    display_text += '<h4 style="color: #8B4513;">注释：</h4>'
                    for annotation in annotations:
                        display_text += f'<p style="margin: 5px 0;">{annotation}</p>'
                    display_text += '</div>'
                
                display_text += '</div>'
                
                # 显示结果
                self.result_text.append(display_text)
            except Exception as e:
                self.result_text.append(f'<div style="color: #B22222;">第{i+1}首注释失败：{str(e)}</div>')
                continue

    def translate_poem(self):
        """古今对照翻译"""
        try:
            # 生成5首诗词
            poems = []
            for _ in range(5):
                poem = self.translator.get_random_poem()
                poems.append(poem)
            
            # 翻译诗词
            display_text = "古今对照翻译：\n\n"
            for i, poem in enumerate(poems, 1):
                result = self.translator.translate_poem(poem)
                display_text += f"第{i}首：\n"
                display_text += f"原文：{result['original']}\n"
                display_text += f"译文：{result['translation']}\n"
                display_text += f"解释：\n{result['explanation']}\n\n"
            
            self.result_text.setPlainText(display_text)
        except Exception as e:
            logging.error(f"翻译诗词时出错：{str(e)}")
            self.result_text.setPlainText(f"翻译诗词时出错：{str(e)}")

    def resizeEvent(self, event):
        bg_path = "resources/bamboo_bg.jpg"
        if os.path.exists(bg_path):
            palette = self.palette()
            pixmap = QPixmap(bg_path)
            scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
            self.setPalette(palette)
        super().resizeEvent(event)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        
        # 设置应用程序样式
        app.setStyle('Fusion')
        
        # 创建并显示主窗口
        window = PoemAnalysisSystem()
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        print(f"\n程序运行出错：{str(e)}") 