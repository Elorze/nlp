import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import jieba
import re
from collections import Counter
import logging
from pypinyin import pinyin, Style

class PoemScorer:
    def __init__(self):
        # 加载BERT模型和tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('models/poem_classifier')
        self.model = BertModel.from_pretrained('models/poem_classifier')
        self.model.eval()
        
        # 意象词库
        self.image_words = {
            '自然': ['风', '云', '山', '雨', '雪', '月', '日', '星', '天', '地'],
            '植物': ['花', '草', '树', '竹', '梅', '兰', '菊', '松', '柏', '柳'],
            '动物': ['鸟', '鱼', '虫', '蝶', '燕', '莺', '鹤', '雁', '鹰', '龙'],
            '情感': ['愁', '思', '念', '恨', '爱', '喜', '悲', '欢', '乐', '忧'],
            '动作': ['飞', '舞', '游', '走', '行', '立', '坐', '卧', '望', '听']
        }
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scoring.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def get_bert_embedding(self, text):
        """获取文本的BERT嵌入"""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()

    def calculate_image_score(self, poem):
        """计算意境表达力得分（40分）"""
        words = list(jieba.cut(poem))
        score = 0
        image_count = 0
        has_action = False
        
        # 统计意象词数量
        for word in words:
            for category, image_list in self.image_words.items():
                if word in image_list:
                    image_count += 1
                    if category == '动作':
                        has_action = True
        
        # 计算基础分（意象词数量）
        base_score = min(image_count * 2.5, 30)  # 最多30分
        
        # 动作描写加分
        if has_action:
            score += 10
        
        score += base_score
        return min(score, 40), {
            '意象词数量': image_count,
            '动作描写': '有' if has_action else '无'
        }

    def calculate_theme_score(self, poem):
        """计算主题相关性得分（25分）"""
        try:
            # 将诗词分成句子
            lines = poem.split('\n')
            if len(lines) < 2:
                return 0, {'error': '诗词行数不足'}
            
            # 计算句子间的相似度
            embeddings = [self.get_bert_embedding(line) for line in lines]
            similarities = []
            for i in range(len(embeddings)-1):
                sim = cosine_similarity(embeddings[i], embeddings[i+1])[0][0]
                similarities.append(sim)
            
            # 计算平均相似度
            avg_sim = np.mean(similarities)
            score = avg_sim * 25  # 映射到25分
            
            return score, {'平均相似度': avg_sim}
        except Exception as e:
            logging.error(f"计算主题相关性得分时出错：{str(e)}")
            return 0, {'error': str(e)}

    def calculate_rhyme_score(self, poem):
        """计算韵律感得分（20分）"""
        try:
            lines = poem.split('\n')
            if len(lines) < 2:
                return 0, {'error': '诗词行数不足'}
            
            # 获取每行最后一个字的拼音韵母
            last_chars = [line[-1] for line in lines if line.strip()]
            last_pinyins = [pinyin(char, style=Style.FINALS)[0][0] for char in last_chars]
            
            # 检查是否押韵
            if len(set(last_pinyins)) == 1:  # 所有韵母相同
                return 20, {'押韵情况': '完全押韵'}
            else:
                return 5, {'押韵情况': '不完全押韵'}
        except Exception as e:
            logging.error(f"计算韵律感得分时出错：{str(e)}")
            return 0, {'error': str(e)}

    def calculate_structure_score(self, poem):
        """计算对仗或结构得分（15分）"""
        try:
            lines = poem.split('\n')
            if len(lines) < 2:
                return 0, {'error': '诗词行数不足'}
            
            score = 0
            analysis = []
            
            # 检查字数是否相同
            lengths = [len(line.strip()) for line in lines]
            if len(set(lengths)) == 1:
                score += 8
                analysis.append('字数整齐')
            
            # 简单检查对仗（这里只是示例，实际对仗检查更复杂）
            if len(lines) >= 2:
                line1_words = list(jieba.cut(lines[0]))
                line2_words = list(jieba.cut(lines[1]))
                if len(line1_words) == len(line2_words):
                    score += 7
                    analysis.append('有对仗倾向')
            
            return score, {'分析': '、'.join(analysis) if analysis else '无对仗结构'}
        except Exception as e:
            logging.error(f"计算结构得分时出错：{str(e)}")
            return 0, {'error': str(e)}

    def score_poem(self, poem):
        """综合评分"""
        try:
            # 计算各项得分
            image_score, image_analysis = self.calculate_image_score(poem)
            theme_score, theme_analysis = self.calculate_theme_score(poem)
            rhyme_score, rhyme_analysis = self.calculate_rhyme_score(poem)
            structure_score, structure_analysis = self.calculate_structure_score(poem)
            
            # 汇总得分
            scores = {
                '意境表达力': image_score,
                '主题相关性': theme_score,
                '韵律感': rhyme_score,
                '对仗结构': structure_score
            }
            
            # 计算总分
            total_score = sum(scores.values())
            
            # 汇总分析
            analysis = {
                '意境分析': f"意象词数量：{image_analysis['意象词数量']}，动作描写：{image_analysis['动作描写']}",
                '主题分析': f"句子相似度：{theme_analysis.get('平均相似度', 'N/A'):.2f}",
                '韵律分析': rhyme_analysis['押韵情况'],
                '结构分析': structure_analysis['分析']
            }
            
            return {
                'scores': scores,
                'total_score': total_score,
                'analysis': analysis
            }
        except Exception as e:
            logging.error(f"评分过程出错：{str(e)}")
            return {
                'scores': {'error': str(e)},
                'total_score': 0,
                'analysis': {'error': str(e)}
            }

def main():
    scorer = PoemScorer()
    
    # 测试诗词
    test_poem = """
    春眠不觉晓
    处处闻啼鸟
    夜来风雨声
    花落知多少
    """
    
    # 评分
    result = scorer.score_poem(test_poem)
    
    # 输出结果
    print("诗词评分结果：")
    print(f"总分：{result['total_score']:.2f}")
    print("\n分项得分：")
    for key, value in result['scores'].items():
        print(f"{key}: {value:.2f}")
    print("\n分析：")
    for key, value in result['analysis'].items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main() 