import pypinyin
from config.poem_config import PoemConfig

class RhymeChecker:
    def __init__(self):
        self.config = PoemConfig()
    
    def get_tone(self, char):
        """
        获取单个汉字的声调
        :param char: 汉字
        :return: 声调类型（阴平、阳平、上声、去声、入声）
        """
        pinyin = pypinyin.lazy_pinyin(char, style=pypinyin.STYLE_TONE3)[0]
        tone = pinyin[-1]
        
        if tone == '1':
            return "阴平"
        elif tone == '2':
            return "阳平"
        elif tone == '3':
            return "上声"
        elif tone == '4':
            return "去声"
        else:
            return "入声"
    
    def check_tone(self, text):
        """
        检查文本的平仄
        :param text: 输入文本
        :return: 平仄检查结果
        """
        result = []
        for char in text:
            if char in ['，', '。', '！', '？', '、']:
                continue
            tone = self.get_tone(char)
            result.append({
                "char": char,
                "tone": tone,
                "type": "平声" if tone in self.config.TONE_RULES["平声"] else "仄声"
            })
        return result
    
    def check_rhyme(self, text):
        """
        检查文本的押韵
        :param text: 输入文本
        :return: 押韵检查结果
        """
        # 获取韵脚
        lines = [line.strip() for line in text.split('。') if line.strip()]
        rhymes = []
        
        for line in lines:
            if not line:
                continue
            # 获取每行最后一个非标点字符
            last_char = None
            for char in reversed(line):
                if char not in ['，', '。', '！', '？', '、']:
                    last_char = char
                    break
            if last_char:
                pinyin = pypinyin.lazy_pinyin(last_char, style=pypinyin.STYLE_FINALS)[0]
                rhymes.append({
                    "char": last_char,
                    "rhyme": pinyin
                })
        
        # 检查是否押韵（第二、四句押韵）
        is_rhyming = True
        if len(rhymes) >= 4:
            if rhymes[1]["rhyme"] != rhymes[3]["rhyme"]:
                is_rhyming = False
        
        return {
            "rhymes": rhymes,
            "is_rhyming": is_rhyming
        }
    
    def check_wuyan_jujue(self, text):
        """
        检查是否符合五言绝句的平仄格式
        :param text: 输入文本
        :return: 检查结果
        """
        # 移除标点符号
        clean_text = ''.join([char for char in text if char not in ['，', '。', '！', '？', '、']])
        
        # 检查是否为20字
        if len(clean_text) != 20:
            return {
                "is_valid": False,
                "reason": "字数不符合五言绝句要求（应为20字）",
                "actual_pattern": "",
                "standard_patterns": self.config.WUYAN_JUJUE_PATTERNS,
                "tone_details": []
            }
        
        # 检查平仄
        tone_result = self.check_tone(clean_text)
        actual_pattern = ''.join(['平' if item["type"] == "平声" else '仄' for item in tone_result])
        
        # 将实际平仄格式转换为便于比较的格式
        formatted_pattern = ''
        for i in range(0, len(actual_pattern), 5):
            formatted_pattern += actual_pattern[i:i+5]
            if i < 15:  # 不是最后一组
                formatted_pattern += '，' if (i // 5) % 2 == 0 else '。'
        formatted_pattern += '。'
        
        # 检查是否符合标准格式
        is_valid = formatted_pattern in self.config.WUYAN_JUJUE_PATTERNS
        
        return {
            "is_valid": is_valid,
            "actual_pattern": formatted_pattern,
            "standard_patterns": self.config.WUYAN_JUJUE_PATTERNS,
            "tone_details": tone_result
        } 