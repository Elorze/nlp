# 古诗词分类器

这是一个基于机器学习的古诗词分类系统，可以对古诗词进行自动分类。

## 功能特点

- 支持对古诗词进行自动分类（山水、咏史、送别等类别）
- 使用jieba分词进行中文分词
- 采用TF-IDF特征提取
- 使用SVM分类器进行训练
- 提供预测概率分布

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 准备训练数据（CSV格式，包含content和label两列）
2. 训练模型：
```python
from poem_classifier import PoemClassifier

classifier = PoemClassifier()
classifier.train('data/your_data.csv')
```

3. 预测新诗词：
```python
result = classifier.predict("你的诗词内容")
print(result['label'])  # 输出分类结果
print(result['probabilities'])  # 输出各类别概率
```

## 项目结构

- `poem_classifier.py`: 主要的分类器实现
- `data/`: 存放训练数据
- `models/`: 存放训练好的模型
- `requirements.txt`: 项目依赖

## 作者

Elorze

## 许可证

MIT License 