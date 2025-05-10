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

# 过滤警告
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=UndefinedMetricWarning)

class PoemClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(tokenizer=self._tokenize)
        self.classifier = SVC(kernel='linear', probability=True)
        self.labels = ['山水', '咏史', '送别']
        
        # 确保必要的目录存在
        os.makedirs('data', exist_ok=True)
        os.makedirs('models', exist_ok=True)
        
    def _tokenize(self, text):
        # 使用jieba分词
        return list(jieba.cut(text))
    
    def train(self, data_path='data/example_poems.csv'):
        try:
            # 检查数据文件是否存在
            if not os.path.exists(data_path):
                raise FileNotFoundError(f"数据文件 {data_path} 不存在")
                
            # 尝试不同的编码方式读取数据
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
                
            X = df['content'].values
            y = df['label'].values
            
            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # 特征提取
            X_train_tfidf = self.vectorizer.fit_transform(X_train)
            X_test_tfidf = self.vectorizer.transform(X_test)
            
            # 训练模型
            self.classifier.fit(X_train_tfidf, y_train)
            
            # 评估模型
            y_pred = self.classifier.predict(X_test_tfidf)
            print("\n分类器评估报告：")
            print(classification_report(y_test, y_pred, target_names=self.labels))
            
            # 保存模型
            self._save_model()
            print("\n模型训练完成并保存")
            
        except Exception as e:
            print(f"\n训练过程中出现错误：{str(e)}")
            raise
        
    def predict(self, poem):
        try:
            # 加载模型（如果存在）
            if not hasattr(self, 'classifier') or not hasattr(self, 'vectorizer'):
                self._load_model()
                
            # 特征提取
            X_tfidf = self.vectorizer.transform([poem])
            
            # 预测
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
        try:
            # 保存模型和向量器
            with open('models/classifier.pkl', 'wb') as f:
                pickle.dump(self.classifier, f)
                
            with open('models/vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizer, f)
        except Exception as e:
            print(f"\n保存模型时出现错误：{str(e)}")
            raise
            
    def _load_model(self):
        try:
            # 检查模型文件是否存在
            if not os.path.exists('models/classifier.pkl') or not os.path.exists('models/vectorizer.pkl'):
                raise FileNotFoundError("模型文件不存在，请先训练模型")
                
            # 加载模型和向量器
            with open('models/classifier.pkl', 'rb') as f:
                self.classifier = pickle.load(f)
                
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
        
        # 测试一些示例
        test_poems = [
            "春眠不觉晓处处闻啼鸟夜来风雨声花落知多少",
            "秦时明月汉时关万里长征人未还但使龙城飞将在不教胡马度阴山",
            "渭城朝雨浥轻尘客舍青青柳色新劝君更尽一杯酒西出阳关无故人"
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