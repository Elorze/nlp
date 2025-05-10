import jieba
import jieba.posseg as pseg
from collections import defaultdict

class ImageExtractor:
    def __init__(self):
        # 意象词词典
        self.image_dict = {
            "自然景物": ["山", "水", "云", "月", "花", "草", "树", "风", "雨", "雪"],
            "人物": ["人", "君", "客", "友", "子", "郎", "女", "士", "僧", "道"],
            "情感": ["愁", "思", "念", "悲", "喜", "忧", "恨", "爱", "怨", "欢"]
        }
        
        # 加载自定义词典
        for word in sum(self.image_dict.values(), []):
            jieba.add_word(word)
    
    def extract(self, text):
        words = pseg.cut(text)
        result = defaultdict(list)
        
        for word, flag in words:
            for category, images in self.image_dict.items():
                if word in images:
                    result[category].append(word)
        
        return dict(result)
    
    def add_image_word(self, category, word):
        if category in self.image_dict:
            self.image_dict[category].append(word)
            jieba.add_word(word) 