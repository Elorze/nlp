"""
诗词生成技术流程图：
随机主题词 -> GPT-2模型 -> 生成诗词 -> 格式化输出

技术说明：
1. 模型架构：基于 Transformer 的 GPT-2 模型
   - 基础架构：Transformer（提供并行处理和自注意力机制）
   - 具体实现：GPT-2（使用Transformer的decoder部分，用于文本生成）
   - 应用版本：uer/gpt2-chinese-poem（针对中文诗词的GPT-2模型）
   - 核心组件：
     * BertTokenizer：进行分词处理
       - 作用：将输入文本转换为模型可以理解的数字序列
       - 处理流程：文本 -> 分词 -> 转换为ID -> 添加特殊标记
       - 与GPT2LMHeadModel的关系：为模型提供标准化的输入格式
     * GPT2LMHeadModel：进行诗词生成
       - 作用：基于输入序列生成新的诗词文本
       - 处理流程：接收token序列 -> 通过decoder层处理 -> 生成下一个token
       - 与BertTokenizer的关系：
         * 输入：接收tokenizer处理后的数字序列
         * 输出：生成的是数字序列（token IDs）
         * 解码过程：需要tokenizer将数字序列转换回可读的文本
         * 实际应用：在generate_poem函数中，使用tokenizer.decode(output[0])将模型输出转换为诗词文本
       - 预测过程通俗解释：
         * 第一步：每个汉字都有一个对应的数字编号（比如"春"可能是100，"风"可能是200）
         * 第二步：模型看到前面的数字序列，比如"100 200"（"春风"）
         * 第三步：模型根据这些数字，计算下一个最可能出现的数字
         * 第四步：这个数字对应一个汉字，就是预测的下一个字
         * 实际例子：
           - 输入："春风"（数字：100 200）
           - 模型计算后可能预测：300（对应"吹"）
           - 最终生成："春风吹"
   - 工作原理：根据前面的文字预测下一个最合适的字/词
   - 生成过程：输入主题词 -> 预测下一个字 -> 预测下一个字 -> ... -> 生成完整诗词

2. Transformer 架构特点
   - 核心特点：可以同时处理整个序列，而不是一个接一个处理
   - 实现方式：通过位置编码和自注意力机制
   - 并行处理原理：
     * 位置编码：给每个位置添加独特的编码，让模型知道词的位置信息
     * 自注意力机制：同时计算所有词之间的关系，不需要等待前面的处理完成
     * 矩阵运算：可以并行计算所有关系，提高效率
   - 优势：能够捕捉长距离依赖，训练效率高，适合处理中文诗词

3. 通过 torch 深度学习框架实现
   - 模型管理：加载预训练模型，管理模型参数，控制模型状态
   - 数据处理：文本转换为张量，数据格式转换，批处理操作
   - 计算加速：GPU支持，并行计算，内存优化
   - 模型推理：生成诗词，计算文本相似度，评分分析
   - 性能优化：内存管理，计算效率，批处理支持

4. 生成参数说明：
   - temperature: 0.7 (控制生成的随机性)
   - top_k: 50 (保留概率最高的50个词)
   - top_p: 0.95 (累积概率阈值)
   - no_repeat_ngram_size: 2 (避免重复)
"""

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