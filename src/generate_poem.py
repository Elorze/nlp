import torch
from transformers import GPT2LMHeadModel, BertTokenizer
import logging
import os
import sys
import random

# 添加当前目录到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from poem_scorer import PoemScorer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('generation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def generate_poem():
    """生成诗词"""
    try:
        # 设置设备
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logging.info(f'使用设备: {device}')
        
        # 加载预训练模型和分词器
        logging.info('加载模型和分词器...')
        model_name = 'uer/gpt2-chinese-poem'
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        model.to(device)
        model.eval()
        
        # 设置生成参数
        input_text = random.choice(['春', '夏', '秋', '冬', '月', '风', '花', '雪'])
        input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
        
        # 生成诗词
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=50,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7,
                pad_token_id=tokenizer.pad_token_id
            )
        
        # 解码生成的文本
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # 格式化输出
        poem = format_poem(generated_text)
        
        logging.info("成功生成新诗词")
        return poem
    except Exception as e:
        error_msg = f"生成诗词失败：{str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

def format_poem(text):
    """格式化诗词"""
    try:
        # 移除多余的空格和换行
        text = text.strip()
        
        # 如果文本长度不是20的倍数，截取到最近的20的倍数
        if len(text) % 20 != 0:
            text = text[:len(text) - (len(text) % 20)]
        
        # 每5个字符添加一个换行
        lines = []
        for i in range(0, len(text), 5):
            if i + 5 <= len(text):
                lines.append(text[i:i+5])
        
        # 确保是4行
        while len(lines) < 4:
            lines.append("     ")
        lines = lines[:4]
        
        return "\n".join(lines)
    except Exception as e:
        error_msg = f"格式化诗词失败：{str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

def main():
    try:
        # 设置设备
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logging.info(f'Using device: {device}')
        
        # 加载预训练模型和分词器
        logging.info('Loading model and tokenizer...')
        model_name = 'uer/gpt2-chinese-poem'
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        model.to(device)
        logging.info('Model and tokenizer loaded successfully')
        
        # 初始化评分器
        logging.info('Initializing poem scorer...')
        scorer = PoemScorer()
        logging.info('Poem scorer initialized successfully')
        
        # 生成五首诗歌并评分
        print('\n生成的古诗及其评分:')
        for i in range(5):
            print(f'\n第 {i+1} 首:')
            poem = generate_poem()
            print(poem)
            
            # 评分
            scores = scorer.score_poem(poem)
            print("\n评分结果:")
            for metric, score in scores.items():
                print(f"{metric}: {score:.2f}分")
            print("-" * 50)
        
        logging.info('Poems generated and scored successfully')
        
    except Exception as e:
        logging.error(f'Error occurred: {str(e)}')
        raise

if __name__ == '__main__':
    main() 