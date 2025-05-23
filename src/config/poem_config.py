"""
诗词相关配置
"""

class PoemConfig:
    # 意象词分类
    IMAGE_WORDS = {
        "自然景物": [
            "山", "水", "云", "雨", "风", "月", "花", "草", "树", "鸟",
            "江", "河", "湖", "海", "天", "地", "日", "星", "雪", "霜",
            "石", "林", "叶", "枫", "岭", "峰", "溪", "泉", "春", "夏",
            "秋", "冬", "晓", "暮", "晨", "昏", "寒", "暑", "凉", "温"
        ],
        "人物": [
            "人", "君", "臣", "子", "女", "客", "友", "僧", "道", "仙",
            "士", "农", "工", "商", "父", "母", "兄", "弟", "姐", "妹",
            "翁", "妇", "郎", "妾", "夫", "妻", "师", "徒", "主", "仆"
        ],
        "情感": [
            "愁", "思", "念", "忧", "喜", "悲", "欢", "乐", "哀", "怒",
            "爱", "恨", "情", "意", "心", "怀", "感", "伤", "痛", "苦",
            "愁", "思", "念", "忧", "喜", "悲", "欢", "乐", "哀", "怒",
            "愁", "思", "念", "忧", "喜", "悲", "欢", "乐", "哀", "怒"
        ]
    }
    
    # 平仄规则
    TONE_RULES = {
        "平声": ["阴平", "阳平"],
        "仄声": ["上声", "去声", "入声"]
    }
    
    # 韵部规则
    RHYME_RULES = {
        "平水韵": {
            "一东": ["东", "同", "童", "僮", "铜", "桐", "峒", "筒", "瞳", "中"],
            "二冬": ["冬", "咚", "彤", "农", "侬", "宗", "淙", "锺", "龙", "舂"],
            "三江": ["江", "窗", "香", "乡", "长", "张", "章", "昌", "常", "房"],
            "四支": ["支", "时", "知", "诗", "之", "思", "为", "诗", "宜", "怡"],
            "五微": ["微", "非", "飞", "辉", "违", "围", "归", "依", "机", "衣"]
        }
    }
    
    # 五言绝句平仄格式
    WUYAN_JUJUE_PATTERNS = [
        "仄仄平平仄，平平仄仄平。平平平仄仄，仄仄仄平平。",
        "平平仄仄平，仄仄仄平平。仄仄平平仄，平平仄仄平。"
    ] 