from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import os

class PoetryGenerator:
    def __init__(self):
        self.model_path = "models/generator"
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        
        # 如果模型已经训练好，加载模型
        if os.path.exists(self.model_path):
            self.model.load_state_dict(torch.load(os.path.join(self.model_path, "pytorch_model.bin")))
    
    def generate(self, theme):
        # 设置生成参数
        input_text = f"主题：{theme}\n生成五言绝句："
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        
        # 生成诗词
        output = self.model.generate(
            input_ids,
            max_length=100,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text
    
    def train(self, poetry_data):
        # 训练模型的代码将在后续实现
        pass 