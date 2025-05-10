import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import jieba
import logging
from collections import Counter
from pyhanlp import *
import os

class EmotionAnalyzer:
    def __init__(self):
        try:
            logging.info("开始初始化情感分析器...")
            
            # 加载BERT模型和tokenizer
            logging.info("正在加载BERT模型和tokenizer...")
            model_path = 'models/poem_classifier'
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"模型路径不存在：{model_path}")
            
            self.tokenizer = BertTokenizer.from_pretrained(model_path)
            self.model = BertModel.from_pretrained(model_path)
            self.model.eval()
            logging.info("BERT模型和tokenizer加载完成")
            
            # 重构情感类别
            self.emotion_categories = {
                '思乡': {
                    'keywords': ['乡', '家', '归', '故', '亲', '念', '忆', '怀', '望', '思'],
                    'imagery': ['明月', '长亭', '归雁', '羁旅', '客舍', '故园', '乡关', '归心']
                },
                '哀伤': {
                    'keywords': ['愁', '悲', '泪', '伤', '痛', '苦', '哀', '怨', '恨', '泣'],
                    'imagery': ['寒雨', '孤舟', '霜', '残月', '落花', '寒江', '暮色', '秋雨']
                },
                '孤独': {
                    'keywords': ['独', '孤', '寂', '寞', '冷', '寒', '清', '静', '空', '远'],
                    'imagery': ['孤灯', '寒窗', '空山', '独坐', '孤影', '寒夜', '清秋', '空庭']
                },
                '欢快': {
                    'keywords': ['喜', '乐', '欢', '笑', '歌', '舞', '醉', '兴', '畅', '悦'],
                    'imagery': ['黄鹂', '翠柳', '青天', '白鹭', '春色', '花开', '莺啼', '蝶舞']
                },
                '豪情': {
                    'keywords': ['怒', '愤', '恨', '怨', '仇', '敌', '战', '斗', '争', '抗'],
                    'imagery': ['剑', '楼', '关山', '长城', '战马', '烽火', '铁衣', '金戈']
                },
                '清静': {
                    'keywords': ['闲', '静', '淡', '雅', '幽', '清', '远', '空', '禅', '悟'],
                    'imagery': ['竹林', '溪水', '山寺', '白云', '松风', '明月', '清泉', '远山']
                }
            }
            logging.info("情感类别初始化完成")
            
            # 配置日志
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('emotion_analysis.log', encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )
            logging.info("情感分析器初始化完成")
            
        except Exception as e:
            logging.error(f"情感分析器初始化失败：{str(e)}")
            raise

    def get_bert_embedding(self, text):
        """获取文本的BERT嵌入"""
        try:
            logging.info(f"正在获取文本的BERT嵌入：{text[:20]}...")
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
            with torch.no_grad():
                outputs = self.model(**inputs)
            return outputs.last_hidden_state.mean(dim=1).numpy()
        except Exception as e:
            logging.error(f"获取BERT嵌入失败：{str(e)}")
            raise

    def extract_imagery_and_emotions(self, poem):
        """使用HanLP提取意象词并标注情感"""
        try:
            logging.info(f"正在提取意象词：{poem[:20]}...")
            # 使用HanLP进行词性标注
            words = HanLP.segment(poem)
            imagery_emotions = []
            
            for word in words:
                word_text = str(word.word)
                # 检查是否是意象词
                for emotion, data in self.emotion_categories.items():
                    if word_text in data['imagery']:
                        imagery_emotions.append((word_text, emotion))
            
            logging.info(f"提取到{len(imagery_emotions)}个意象词")
            return imagery_emotions
        except Exception as e:
            logging.error(f"提取意象词失败：{str(e)}")
            raise

    def analyze_emotion(self, poem):
        """分析诗词情感"""
        try:
            logging.info(f"开始分析诗词情感：{poem[:20]}...")
            
            # 1. 提取意象词及其情感
            imagery_emotions = self.extract_imagery_and_emotions(poem)
            
            # 2. 基于意象词的情感分析
            emotion_scores = {emotion: 0 for emotion in self.emotion_categories.keys()}
            for _, emotion in imagery_emotions:
                emotion_scores[emotion] += 1
            
            # 3. 基于BERT的语义分析
            poem_embedding = self.get_bert_embedding(poem)
            emotion_embeddings = {}
            for emotion, data in self.emotion_categories.items():
                # 将情感关键词和意象词组合成文本
                emotion_text = ' '.join(data['keywords'] + data['imagery'])
                emotion_embedding = self.get_bert_embedding(emotion_text)
                # 计算相似度
                similarity = cosine_similarity(poem_embedding, emotion_embedding)[0][0]
                emotion_embeddings[emotion] = similarity

            # 4. 综合两种方法的结果
            final_scores = {}
            for emotion in self.emotion_categories.keys():
                # 意象词得分和语义相似度的加权平均
                imagery_score = emotion_scores[emotion] / len(imagery_emotions) if imagery_emotions else 0
                semantic_score = emotion_embeddings[emotion]
                final_scores[emotion] = 0.6 * imagery_score + 0.4 * semantic_score

            # 5. 获取主要情感和辅助情感
            sorted_emotions = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
            main_emotion = sorted_emotions[0][0]
            secondary_emotion = sorted_emotions[1][0] if len(sorted_emotions) > 1 else None

            # 6. 生成分析报告
            analysis = self.generate_analysis(main_emotion, secondary_emotion, imagery_emotions, final_scores)
            
            logging.info(f"情感分析完成，主要情感：{main_emotion}")

            return {
                'main_emotion': main_emotion,
                'secondary_emotion': secondary_emotion,
                'imagery_emotions': imagery_emotions,
                'emotion_scores': final_scores,
                'analysis': analysis
            }
        except Exception as e:
            logging.error(f"情感分析失败：{str(e)}")
            return {
                'main_emotion': '未知',
                'secondary_emotion': None,
                'imagery_emotions': [],
                'emotion_scores': {},
                'analysis': f"分析失败：{str(e)}"
            }

    def generate_analysis(self, main_emotion, secondary_emotion, imagery_emotions, scores):
        """生成分析报告"""
        try:
            analysis = []
            
            # 主要情感分析
            analysis.append(f"主要情感：{main_emotion}")
            if secondary_emotion:
                analysis.append(f"辅助情感：{secondary_emotion}")
            
            # 意象词分析
            if imagery_emotions:
                analysis.append("\n意象分析：")
                for imagery, emotion in imagery_emotions:
                    analysis.append(f"「{imagery}」（{emotion}）")
            
            # 情感分布分析
            analysis.append("\n情感分布：")
            # 只显示前两个主要情感
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
            for emotion, score in sorted_scores:
                analysis.append(f"{emotion}: {score:.2f}")
            
            return "\n".join(analysis)
        except Exception as e:
            logging.error(f"生成分析报告失败：{str(e)}")
            return f"生成分析报告失败：{str(e)}"

def main():
    try:
        analyzer = EmotionAnalyzer()
        
        # 测试诗词
        test_poem = """
        两个黄鹂鸣翠柳
        一行白鹭上青天
        窗含西岭千秋雪
        门泊东吴万里船
        """
        
        # 分析情感
        result = analyzer.analyze_emotion(test_poem)
        
        # 输出结果
        print("诗词情感分析结果：")
        print(f"主要情感：{result['main_emotion']}")
        if result['secondary_emotion']:
            print(f"辅助情感：{result['secondary_emotion']}")
        print("\n详细分析：")
        print(result['analysis'])
    except Exception as e:
        logging.error(f"主程序运行失败：{str(e)}")
        raise

if __name__ == "__main__":
    main() 