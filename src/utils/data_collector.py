import os
import pandas as pd
from tqdm import tqdm
import json

class DataCollector:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def collect_classification_data(self):
        """收集诗词分类数据"""
        poems_data = []
        
        # 山水类诗词
        landscape_poems = [
            {"title": "望庐山瀑布", "content": "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。", "category": "山水"},
            {"title": "山行", "content": "远上寒山石径斜，白云生处有人家。停车坐爱枫林晚，霜叶红于二月花。", "category": "山水"},
            {"title": "江雪", "content": "千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。", "category": "山水"},
            {"title": "望岳", "content": "岱宗夫如何？齐鲁青未了。造化钟神秀，阴阳割昏晓。荡胸生曾云，决眦入归鸟。会当凌绝顶，一览众山小。", "category": "山水"},
            {"title": "春江花月夜", "content": "春江潮水连海平，海上明月共潮生。滟滟随波千万里，何处春江无月明。", "category": "山水"},
            {"title": "望天门山", "content": "天门中断楚江开，碧水东流至此回。两岸青山相对出，孤帆一片日边来。", "category": "山水"},
            {"title": "早发白帝城", "content": "朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不住，轻舟已过万重山。", "category": "山水"},
            {"title": "望洞庭", "content": "湖光秋月两相和，潭面无风镜未磨。遥望洞庭山水翠，白银盘里一青螺。", "category": "山水"},
            {"title": "鹿柴", "content": "空山不见人，但闻人语响。返景入深林，复照青苔上。", "category": "山水"},
            {"title": "鸟鸣涧", "content": "人闲桂花落，夜静春山空。月出惊山鸟，时鸣春涧中。", "category": "山水"},
            {"title": "山中", "content": "荆溪白石出，天寒红叶稀。山路元无雨，空翠湿人衣。", "category": "山水"},
            {"title": "竹里馆", "content": "独坐幽篁里，弹琴复长啸。深林人不知，明月来相照。", "category": "山水"},
            {"title": "终南别业", "content": "中岁颇好道，晚家南山陲。兴来每独往，胜事空自知。", "category": "山水"},
            {"title": "过故人庄", "content": "故人具鸡黍，邀我至田家。绿树村边合，青山郭外斜。", "category": "山水"},
            {"title": "望洞庭湖赠张丞相", "content": "八月湖水平，涵虚混太清。气蒸云梦泽，波撼岳阳城。", "category": "山水"},
            {"title": "宿建德江", "content": "移舟泊烟渚，日暮客愁新。野旷天低树，江清月近人。", "category": "山水"},
            {"title": "山居秋暝", "content": "空山新雨后，天气晚来秋。明月松间照，清泉石上流。", "category": "山水"},
            {"title": "终南山", "content": "太乙近天都，连山接海隅。白云回望合，青霭入看无。", "category": "山水"},
            {"title": "汉江临眺", "content": "楚塞三湘接，荆门九派通。江流天地外，山色有无中。", "category": "山水"},
            {"title": "望庐山瀑布", "content": "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。", "category": "山水"}
        ]
        
        # 咏史类诗词
        history_poems = [
            {"title": "赤壁", "content": "折戟沉沙铁未销，自将磨洗认前朝。东风不与周郎便，铜雀春深锁二乔。", "category": "咏史"},
            {"title": "蜀相", "content": "丞相祠堂何处寻，锦官城外柏森森。映阶碧草自春色，隔叶黄鹂空好音。", "category": "咏史"},
            {"title": "乌衣巷", "content": "朱雀桥边野草花，乌衣巷口夕阳斜。旧时王谢堂前燕，飞入寻常百姓家。", "category": "咏史"},
            {"title": "登幽州台歌", "content": "前不见古人，后不见来者。念天地之悠悠，独怆然而涕下。", "category": "咏史"},
            {"title": "咏怀古迹", "content": "群山万壑赴荆门，生长明妃尚有村。一去紫台连朔漠，独留青冢向黄昏。", "category": "咏史"},
            {"title": "过华清宫", "content": "长安回望绣成堆，山顶千门次第开。一骑红尘妃子笑，无人知是荔枝来。", "category": "咏史"},
            {"title": "金陵怀古", "content": "潮满冶城渚，日斜征虏亭。蔡洲新草绿，幕府旧烟青。", "category": "咏史"},
            {"title": "台城", "content": "江雨霏霏江草齐，六朝如梦鸟空啼。无情最是台城柳，依旧烟笼十里堤。", "category": "咏史"},
            {"title": "隋宫", "content": "紫泉宫殿锁烟霞，欲取芜城作帝家。玉玺不缘归日角，锦帆应是到天涯。", "category": "咏史"},
            {"title": "马嵬", "content": "海外徒闻更九州，他生未卜此生休。空闻虎旅传宵柝，无复鸡人报晓筹。", "category": "咏史"},
            {"title": "贾生", "content": "宣室求贤访逐臣，贾生才调更无伦。可怜夜半虚前席，不问苍生问鬼神。", "category": "咏史"},
            {"title": "隋宫", "content": "乘兴南游不戒严，九重谁省谏书函。春风举国裁宫锦，半作障泥半作帆。", "category": "咏史"},
            {"title": "咏史", "content": "历览前贤国与家，成由勤俭破由奢。何须琥珀方为枕，岂得真珠始是车。", "category": "咏史"},
            {"title": "金陵怀古", "content": "辇路江枫暗，宫庭野草春。伤心庾开府，老作北朝臣。", "category": "咏史"},
            {"title": "咏怀古迹", "content": "摇落深知宋玉悲，风流儒雅亦吾师。怅望千秋一洒泪，萧条异代不同时。", "category": "咏史"},
            {"title": "咏怀古迹", "content": "诸葛大名垂宇宙，宗臣遗像肃清高。三分割据纡筹策，万古云霄一羽毛。", "category": "咏史"},
            {"title": "咏怀古迹", "content": "群山万壑赴荆门，生长明妃尚有村。一去紫台连朔漠，独留青冢向黄昏。", "category": "咏史"},
            {"title": "咏怀古迹", "content": "蜀主窥吴幸三峡，崩年亦在永安宫。翠华想像空山里，玉殿虚无野寺中。", "category": "咏史"},
            {"title": "咏怀古迹", "content": "诸葛大名垂宇宙，宗臣遗像肃清高。三分割据纡筹策，万古云霄一羽毛。", "category": "咏史"},
            {"title": "咏怀古迹", "content": "伯仲之间见伊吕，指挥若定失萧曹。运移汉祚终难复，志决身歼军务劳。", "category": "咏史"}
        ]
        
        # 送别类诗词
        farewell_poems = [
            {"title": "送元二使安西", "content": "渭城朝雨浥轻尘，客舍青青柳色新。劝君更尽一杯酒，西出阳关无故人。", "category": "送别"},
            {"title": "送杜少府之任蜀州", "content": "城阙辅三秦，风烟望五津。与君离别意，同是宦游人。", "category": "送别"},
            {"title": "送孟浩然之广陵", "content": "故人西辞黄鹤楼，烟花三月下扬州。孤帆远影碧空尽，唯见长江天际流。", "category": "送别"},
            {"title": "芙蓉楼送辛渐", "content": "寒雨连江夜入吴，平明送客楚山孤。洛阳亲友如相问，一片冰心在玉壶。", "category": "送别"},
            {"title": "送别", "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。", "category": "送别"},
            {"title": "送友人", "content": "青山横北郭，白水绕东城。此地一为别，孤蓬万里征。", "category": "送别"},
            {"title": "送别", "content": "下马饮君酒，问君何所之。君言不得意，归卧南山陲。", "category": "送别"},
            {"title": "送别", "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。", "category": "送别"},
            {"title": "送别", "content": "下马饮君酒，问君何所之。君言不得意，归卧南山陲。", "category": "送别"},
            {"title": "送别", "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。", "category": "送别"},
            {"title": "送别", "content": "下马饮君酒，问君何所之。君言不得意，归卧南山陲。", "category": "送别"},
            {"title": "送别", "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。", "category": "送别"},
            {"title": "送别", "content": "下马饮君酒，问君何所之。君言不得意，归卧南山陲。", "category": "送别"},
            {"title": "送别", "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。", "category": "送别"},
            {"title": "送别", "content": "下马饮君酒，问君何所之。君言不得意，归卧南山陲。", "category": "送别"},
            {"title": "送别", "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。", "category": "送别"},
            {"title": "送别", "content": "下马饮君酒，问君何所之。君言不得意，归卧南山陲。", "category": "送别"},
            {"title": "送别", "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。", "category": "送别"},
            {"title": "送别", "content": "下马饮君酒，问君何所之。君言不得意，归卧南山陲。", "category": "送别"},
            {"title": "送别", "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。", "category": "送别"}
        ]
        
        poems_data.extend(landscape_poems)
        poems_data.extend(history_poems)
        poems_data.extend(farewell_poems)
        
        # 保存数据
        df = pd.DataFrame(poems_data)
        df.to_csv(os.path.join(self.data_dir, "poem_classification.csv"), index=False, encoding='utf-8')
        return df
    
    def collect_generation_data(self):
        """收集诗词生成训练数据"""
        poems_data = [
            {
                "title": "静夜思",
                "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
                "author": "李白",
                "dynasty": "唐"
            },
            {
                "title": "登鹳雀楼",
                "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
                "author": "王之涣",
                "dynasty": "唐"
            },
            {
                "title": "春晓",
                "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
                "author": "孟浩然",
                "dynasty": "唐"
            },
            {
                "title": "相思",
                "content": "红豆生南国，春来发几枝。愿君多采撷，此物最相思。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "杂诗",
                "content": "君自故乡来，应知故乡事。来日绮窗前，寒梅著花未。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "鹿柴",
                "content": "空山不见人，但闻人语响。返景入深林，复照青苔上。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "竹里馆",
                "content": "独坐幽篁里，弹琴复长啸。深林人不知，明月来相照。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "送别",
                "content": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "鸟鸣涧",
                "content": "人闲桂花落，夜静春山空。月出惊山鸟，时鸣春涧中。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "山中",
                "content": "荆溪白石出，天寒红叶稀。山路元无雨，空翠湿人衣。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "终南别业",
                "content": "中岁颇好道，晚家南山陲。兴来每独往，胜事空自知。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "过故人庄",
                "content": "故人具鸡黍，邀我至田家。绿树村边合，青山郭外斜。",
                "author": "孟浩然",
                "dynasty": "唐"
            },
            {
                "title": "宿建德江",
                "content": "移舟泊烟渚，日暮客愁新。野旷天低树，江清月近人。",
                "author": "孟浩然",
                "dynasty": "唐"
            },
            {
                "title": "山居秋暝",
                "content": "空山新雨后，天气晚来秋。明月松间照，清泉石上流。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "终南山",
                "content": "太乙近天都，连山接海隅。白云回望合，青霭入看无。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "汉江临眺",
                "content": "楚塞三湘接，荆门九派通。江流天地外，山色有无中。",
                "author": "王维",
                "dynasty": "唐"
            },
            {
                "title": "望庐山瀑布",
                "content": "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。",
                "author": "李白",
                "dynasty": "唐"
            },
            {
                "title": "望天门山",
                "content": "天门中断楚江开，碧水东流至此回。两岸青山相对出，孤帆一片日边来。",
                "author": "李白",
                "dynasty": "唐"
            },
            {
                "title": "早发白帝城",
                "content": "朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不住，轻舟已过万重山。",
                "author": "李白",
                "dynasty": "唐"
            },
            {
                "title": "望洞庭",
                "content": "湖光秋月两相和，潭面无风镜未磨。遥望洞庭山水翠，白银盘里一青螺。",
                "author": "刘禹锡",
                "dynasty": "唐"
            }
        ]
        
        # 保存数据
        df = pd.DataFrame(poems_data)
        df.to_csv(os.path.join(self.data_dir, "poem_generation.csv"), index=False, encoding='utf-8')
        return df
    
    def preprocess_data(self):
        """预处理收集到的数据"""
        # 读取分类数据
        classification_df = pd.read_csv(os.path.join(self.data_dir, "poem_classification.csv"))
        
        # 数据清洗
        classification_df = classification_df.dropna()
        classification_df = classification_df.drop_duplicates()
        
        # 保存处理后的数据
        classification_df.to_csv(os.path.join(self.data_dir, "poem_classification_processed.csv"), 
                               index=False, encoding='utf-8')
        
        # 读取生成数据
        generation_df = pd.read_csv(os.path.join(self.data_dir, "poem_generation.csv"))
        
        # 数据清洗
        generation_df = generation_df.dropna()
        generation_df = generation_df.drop_duplicates()
        
        # 保存处理后的数据
        generation_df.to_csv(os.path.join(self.data_dir, "poem_generation_processed.csv"), 
                           index=False, encoding='utf-8')
        
        return classification_df, generation_df 