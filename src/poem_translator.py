import random
import logging
from pyhanlp import *

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('translation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class PoemTranslator:
    def __init__(self):
        # 示例诗词库
        self.example_poems = [
            "千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。",
            "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
            "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
            "两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。",
            "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
            "秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度阴山。",
            "朱雀桥边野草花，乌衣巷口夕阳斜。旧时王谢堂前燕，飞入寻常百姓家。",
            "折戟沉沙铁未销，自将磨洗认前朝。东风不与周郎便，铜雀春深锁二乔。",
            "烟笼寒水月笼沙，夜泊秦淮近酒家。商女不知亡国恨，隔江犹唱后庭花。",
            "渭城朝雨浥轻尘，客舍青青柳色新。劝君更尽一杯酒，西出阳关无故人。"
        ]
        
        # 常见意象词解释
        self.imagery_dict = {
            '明月': '明亮的月亮',
            '寒江': '寒冷的江水',
            '孤舟': '孤独的小船',
            '蓑笠': '蓑衣和斗笠',
            '黄鹂': '黄莺鸟',
            '翠柳': '翠绿的柳树',
            '白鹭': '白色的鹭鸟',
            '青天': '蓝色的天空',
            '千秋雪': '千年不化的积雪',
            '万里船': '远行的船只',
            '春眠': '春天的睡眠',
            '啼鸟': '鸣叫的鸟儿',
            '风雨': '风和雨',
            '落花': '凋落的花朵',
            '秦时': '秦朝时期',
            '汉时': '汉朝时期',
            '龙城': '边塞重镇',
            '胡马': '胡人的马',
            '朱雀桥': '朱雀桥',
            '乌衣巷': '乌衣巷',
            '王谢': '王导和谢安',
            '堂前燕': '屋檐下的燕子',
            '寻常': '普通',
            '百姓': '平民百姓',
            '折戟': '折断的戟',
            '沉沙': '沉入沙中',
            '铁未销': '铁器还未销蚀',
            '前朝': '前一个朝代',
            '周郎': '周瑜',
            '铜雀': '铜雀台',
            '春深': '春意正浓',
            '二乔': '大乔和小乔',
            '烟笼': '烟雾笼罩',
            '寒水': '寒冷的水',
            '月笼沙': '月光笼罩着沙滩',
            '秦淮': '秦淮河',
            '酒家': '酒店',
            '商女': '歌女',
            '亡国恨': '亡国的悲痛',
            '隔江': '隔着江水',
            '后庭花': '《玉树后庭花》',
            '渭城': '渭城',
            '朝雨': '早晨的雨',
            '浥轻尘': '打湿了轻尘',
            '客舍': '旅店',
            '青青': '青翠',
            '柳色': '柳树的颜色',
            '新': '新鲜',
            '阳关': '阳关',
            '故人': '老朋友'
        }

    def translate_poem(self, poem):
        """翻译诗词为现代白话文"""
        try:
            # 分句
            sentences = poem.replace('，', '。').split('。')
            sentences = [s for s in sentences if s.strip()]
            
            # 翻译结果
            translation = []
            
            for sentence in sentences:
                # 基础翻译
                base_trans = self._translate_sentence(sentence)
                translation.append(base_trans)
            
            return {
                'original': poem,
                'translation': '，'.join(translation) + '。'
            }
        except Exception as e:
            logging.error(f"翻译诗词时出错：{str(e)}")
            raise

    def _translate_sentence(self, sentence):
        """基础翻译"""
        # 替换意象词
        for word, meaning in self.imagery_dict.items():
            if word in sentence:
                sentence = sentence.replace(word, meaning)
        
        # 简单的语法调整
        sentence = sentence.replace('不', '没有')
        sentence = sentence.replace('无', '没有')
        sentence = sentence.replace('独', '独自')
        sentence = sentence.replace('孤', '孤独')
        
        return sentence

    def get_random_poem(self):
        """获取随机诗词"""
        return random.choice(self.example_poems) 