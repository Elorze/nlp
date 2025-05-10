import jieba
from config.poem_config import PoemConfig

class ImageWordExtractor:
    def __init__(self):
        self.config = PoemConfig()
        # 加载自定义词典
        for category, words in self.config.IMAGE_WORDS.items():
            for word in words:
                jieba.add_word(word)
    
    def extract_image_words(self, text):
        """
        从文本中提取意象词
        :param text: 输入文本
        :return: 字典，包含各类别的意象词
        """
        # 分词
        words = jieba.lcut(text)
        
        # 初始化结果字典
        result = {category: [] for category in self.config.IMAGE_WORDS.keys()}
        
        # 识别意象词
        for word in words:
            for category, image_words in self.config.IMAGE_WORDS.items():
                if word in image_words and word not in result[category]:
                    result[category].append(word)
        
        return result
    
    def get_image_word_statistics(self, text):
        """
        获取意象词统计信息
        :param text: 输入文本
        :return: 统计信息字典
        """
        image_words = self.extract_image_words(text)
        
        statistics = {
            "total_words": len(jieba.lcut(text)),
            "image_words_count": sum(len(words) for words in image_words.values()),
            "categories": {}
        }
        
        for category, words in image_words.items():
            statistics["categories"][category] = {
                "count": len(words),
                "words": words
            }
        
        return statistics 