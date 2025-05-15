"""
诗词古今翻译技术流程图：
输入诗词 -> 分句处理 -> 基础翻译 -> 主题识别 -> 修辞分析 -> 意象解释 -> 输出结果
  ↓
分句    意象词替换    主题匹配    修辞匹配    意象匹配
(。，)  (词典)     (关键词)    (模式)     (词典)

技术说明：
1. 翻译方法：
   - 基础翻译：
     * 分句处理：按标点符号分割
     * 意象词替换：使用预定义词典
     * 语法调整：替换常见古语词
   - 主题识别：
     * 使用关键词匹配
     * 识别思乡、送别、咏史等主题
   - 修辞分析：
     * 识别比喻、对仗等修辞手法
     * 提供修辞手法解释
     * 实现方式：
       - 预定义修辞手法词典（比喻、对仗、借景抒情等）
       - 为每种修辞手法定义关键词模式
       - 通过关键词匹配识别修辞手法
       - 提供修辞手法的详细解释
     * 支持的修辞手法：
       - 比喻：通过"如"、"似"、"若"、"像"等词识别
       - 对仗：通过"对仗"、"对偶"等词识别
       - 借景抒情：通过"借景"、"寓情"等词识别
       - 用典：通过"典故"、"引用"等词识别
       - 夸张：通过"夸张"、"夸大"等词识别
   - 意象解释：
     * 识别诗词中的意象词
     * 提供意象词详细解释

2. 使用工具：
   - 预定义词典：意象词、主题、修辞手法
   - 正则表达式：用于分句和模式匹配
   - 日志系统：记录翻译过程

3. NLP技术：
   - 中文分词（HanLP）：
     * 用于分句处理
     * 识别词语边界
   - 词典匹配：
     * 意象词匹配：替换古语词为现代词
     * 主题匹配：识别诗词主题
     * 修辞匹配：识别修辞手法
   - 文本处理：
     * 简单的语法调整
     * 标点符号处理
     * 词语替换
"""

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
        
        # 诗词主题解释
        self.theme_dict = {
            '思乡': '这首诗表达了诗人对故乡的思念之情。',
            '送别': '这是一首送别诗，表达了诗人对离别的感伤和对友人的祝福。',
            '咏史': '这首诗通过历史典故，抒发了诗人对历史的感慨。',
            '山水': '这是一首描写自然山水的诗，展现了诗人对自然的热爱。',
            '抒情': '这首诗主要表达了诗人的情感和感受。'
        }
        
        # 常见修辞手法解释
        self.rhetoric_dict = {
            '比喻': '通过比喻手法，使诗歌更加生动形象。',
            '对仗': '运用对仗手法，使诗歌结构工整，韵律和谐。',
            '借景抒情': '通过描写景物来表达情感。',
            '用典': '运用历史典故，增加诗歌的文化内涵。',
            '夸张': '通过夸张手法，突出诗歌的主题。'
        }

    def translate_poem(self, poem):
        """翻译诗词为现代白话文"""
        try:
            # 分句
            sentences = poem.replace('，', '。').split('。')
            sentences = [s for s in sentences if s.strip()]
            
            # 翻译结果
            translation = []
            explanation = []
            
            # 基础翻译
            for sentence in sentences:
                base_trans = self._translate_sentence(sentence)
                translation.append(base_trans)
            
            # 添加主题解释
            theme = self._identify_theme(poem)
            if theme:
                explanation.append(f"主题：{self.theme_dict.get(theme, '')}")
            
            # 添加修辞手法解释
            rhetoric = self._identify_rhetoric(poem)
            if rhetoric:
                explanation.append(f"修辞：{self.rhetoric_dict.get(rhetoric, '')}")
            
            # 添加意象解释
            imagery = self._identify_imagery(poem)
            if imagery:
                explanation.append("意象分析：")
                for word, meaning in imagery.items():
                    explanation.append(f"- {word}：{meaning}")
            
            return {
                'original': poem,
                'translation': '，'.join(translation) + '。',
                'explanation': '\n'.join(explanation)
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

    def _identify_theme(self, poem):
        """识别诗词主题"""
        themes = {
            '思乡': ['故乡', '思乡', '乡愁', '归家'],
            '送别': ['送别', '离别', '远行', '告别'],
            '咏史': ['历史', '典故', '古人', '往事'],
            '山水': ['山', '水', '云', '雨', '风', '月'],
            '抒情': ['情', '思', '愁', '喜', '悲']
        }
        
        for theme, keywords in themes.items():
            if any(keyword in poem for keyword in keywords):
                return theme
        return None

    def _identify_rhetoric(self, poem):
        """识别修辞手法"""
        rhetoric_patterns = {
            '比喻': ['如', '似', '若', '像'],
            '对仗': ['对仗', '对偶'],
            '借景抒情': ['借景', '寓情'],
            '用典': ['典故', '引用'],
            '夸张': ['夸张', '夸大']
        }
        
        for rhetoric, patterns in rhetoric_patterns.items():
            if any(pattern in poem for pattern in patterns):
                return rhetoric
        return None

    def _identify_imagery(self, poem):
        """识别意象词"""
        imagery = {}
        for word, meaning in self.imagery_dict.items():
            if word in poem:
                imagery[word] = meaning
        return imagery

    def get_random_poem(self):
        """获取随机诗词"""
        return random.choice(self.example_poems) 