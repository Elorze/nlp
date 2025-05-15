"""
TF-IDF（词频-逆文档频率）通俗解释：
1. 词频（TF）：统计每个词在诗中出现的次数
2. 逆文档频率（IDF）：降低常见词（如"的"、"了"）的权重，提高特色词（如"明月"、"青山"）的权重
3. 工作原理：
   - 把每首诗转换成一组数字（向量）
   - 每个数字代表一个词的重要性
   - 通过比较这些数字来判断诗的类别
4. 例如：
   - 山水诗中"明月"、"青山"的权重会很高
   - 送别诗中"离别"、"远行"的权重会很高
   - "的"、"了"等常见词的权重会被降低

5. 具体计算例子：
   对于诗句"西出阳关无故人，劝君更尽一杯酒"：
   - 送别诗得分：0.8 + 0.7 + 0.6 = 2.1（"阳关"、"故人"、"酒"的权重都很高）
   - 山水诗得分：0.1 + 0.1 + 0.1 = 0.3（这些词在山水诗中权重很低）
   - 咏史诗得分：0.3 + 0.3 + 0.3 = 0.9（这些词在咏史诗中权重中等）
   因为送别诗得分最高，所以判断为送别诗

SVM（支持向量机）通俗解释：
1. 作用：找到最佳的分界线，把不同类型的诗分开
2. 工作原理：
   - 学习训练数据中的规律
   - 找到最佳的分界方式
   - 对新的诗进行分类
3. 优势：
   - 分类准确性高
   - 抗干扰能力强
   - 适合处理高维数据

NLP技术流程图：
原始诗词 -> jieba分词 -> 词语列表 -> TF-IDF处理 -> 数值向量 -> SVM分类器 -> 分类结果
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.exceptions import UndefinedMetricWarning
import jieba
import pickle
import os
import warnings

# 过滤警告信息，避免显示不必要的警告
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=UndefinedMetricWarning)

class PoemClassifier:
    """
    诗词分类器类
    使用TF-IDF特征提取和SVM分类器实现诗词分类
    支持山水、咏史、送别三种类型的分类
    """
    def __init__(self):
        # 初始化TF-IDF向量化器，使用自定义的分词函数
        self.vectorizer = TfidfVectorizer(tokenizer=self._tokenize)
        # 初始化SVM分类器，使用线性核函数，启用概率预测
        self.classifier = SVC(kernel='linear', probability=True)
        # 定义分类标签
        self.labels = ['山水', '咏史', '送别']
        
        # 创建必要的目录结构
        os.makedirs('data', exist_ok=True)  # 数据目录
        os.makedirs('models', exist_ok=True)  # 模型保存目录
        
    def _tokenize(self, text):
        """
        使用jieba进行中文分词
        Args:
            text: 输入的中文文本
        Returns:
            分词后的列表
        """
        return list(jieba.cut(text))
    
    def train(self, data_path='data/example_poems.csv'):
        """
        训练分类器模型
        Args:
            data_path: 训练数据文件路径，默认为'data/example_poems.csv'
        Raises:
            FileNotFoundError: 当数据文件不存在时抛出
            ValueError: 当数据文件为空或无法读取时抛出
        """
        try:
            # 检查数据文件是否存在
            if not os.path.exists(data_path):
                raise FileNotFoundError(f"数据文件 {data_path} 不存在")
                
            # 尝试使用不同的编码方式读取数据文件
            encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'utf-16']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(data_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
                    
            if df is None:
                raise ValueError("无法以任何编码方式读取数据文件")
                
            if len(df) == 0:
                raise ValueError("数据文件为空")
                
            # 提取特征和标签
            X = df['content'].values  # 诗词内容
            y = df['label'].values    # 诗词标签
            
            # 划分训练集和测试集，测试集占20%
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # 使用TF-IDF进行特征提取
            X_train_tfidf = self.vectorizer.fit_transform(X_train)
            X_test_tfidf = self.vectorizer.transform(X_test)
            
            # 训练SVM分类器
            self.classifier.fit(X_train_tfidf, y_train)
            
            # 在测试集上评估模型性能
            y_pred = self.classifier.predict(X_test_tfidf)
            print("\n分类器评估报告：")
            print(classification_report(y_test, y_pred, target_names=self.labels))
            
            # 保存训练好的模型
            self._save_model()
            print("\n模型训练完成并保存")
            
        except Exception as e:
            print(f"\n训练过程中出现错误：{str(e)}")
            raise
        
    def predict(self, poem):
        """
        预测单首诗词的类别
        Args:
            poem: 待分类的诗词文本
        Returns:
            dict: 包含预测标签和各类别概率的字典
        """
        try:
            # 如果模型未加载，则加载模型
            if not hasattr(self, 'classifier') or not hasattr(self, 'vectorizer'):
                self._load_model()
                
            # 使用TF-IDF进行特征提取
            X_tfidf = self.vectorizer.transform([poem])
            
            # 预测类别和概率
            label = self.classifier.predict(X_tfidf)[0]
            probabilities = self.classifier.predict_proba(X_tfidf)[0]
            
            return {
                'label': self.labels[label],
                'probabilities': dict(zip(self.labels, probabilities))
            }
        except Exception as e:
            print(f"\n预测过程中出现错误：{str(e)}")
            return None
    
    def _save_model(self):
        """
        保存训练好的模型和向量化器
        将模型保存到models目录下
        """
        try:
            # 保存SVM分类器
            with open('models/classifier.pkl', 'wb') as f:
                pickle.dump(self.classifier, f)
                
            # 保存TF-IDF向量化器
            with open('models/vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizer, f)
        except Exception as e:
            print(f"\n保存模型时出现错误：{str(e)}")
            raise
            
    def _load_model(self):
        """
        加载已保存的模型和向量化器
        从models目录下加载模型文件
        """
        try:
            # 检查模型文件是否存在
            if not os.path.exists('models/classifier.pkl') or not os.path.exists('models/vectorizer.pkl'):
                raise FileNotFoundError("模型文件不存在，请先训练模型")
                
            # 加载SVM分类器
            with open('models/classifier.pkl', 'rb') as f:
                self.classifier = pickle.load(f)
                
            # 加载TF-IDF向量化器
            with open('models/vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
        except Exception as e:
            print(f"\n加载模型时出现错误：{str(e)}")
            raise

if __name__ == '__main__':
    try:
        # 测试分类器
        classifier = PoemClassifier()
        classifier.train()
        
        # 测试一些示例诗词
        test_poems = [
            "春眠不觉晓处处闻啼鸟夜来风雨声花落知多少",  # 山水诗
            "秦时明月汉时关万里长征人未还但使龙城飞将在不教胡马度阴山",  # 咏史诗
            "渭城朝雨浥轻尘客舍青青柳色新劝君更尽一杯酒西出阳关无故人"   # 送别诗
        ]
        
        print("\n测试分类结果：")
        for poem in test_poems:
            result = classifier.predict(poem)
            if result:
                print(f"\n诗词：{poem}")
                print(f"分类结果：{result['label']}")
                print("各类别概率：")
                for label, prob in result['probabilities'].items():
                    print(f"{label}: {prob:.2%}")
    except Exception as e:
        print(f"\n程序运行出错：{str(e)}") 