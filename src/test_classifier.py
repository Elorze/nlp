import torch
from transformers import BertTokenizer, BertForSequenceClassification

def classify_poem(poem):
    """对诗词进行分类"""
    try:
        # 设置设备
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 加载模型和tokenizer
        model = BertForSequenceClassification.from_pretrained('models/poem_classifier')
        model.to(device)
        model.eval()
        
        tokenizer = BertTokenizer.from_pretrained('models/poem_classifier')
        
        # 对输入文本进行编码
        encoding = tokenizer(
            poem,
            add_special_tokens=True,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # 将输入移到设备上
        input_ids = encoding['input_ids'].to(device)
        attention_mask = encoding['attention_mask'].to(device)
        
        # 进行预测
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            _, predicted = torch.max(outputs.logits, 1)
        
        # 获取预测结果
        prediction = predicted.item()
        
        # 生成分类报告
        if prediction == 0:
            category = "抒情诗"
            description = "这首诗属于抒情诗，主要表达诗人的情感和感受。"
        else:
            category = "叙事诗"
            description = "这首诗属于叙事诗，主要讲述故事或描述事件。"
        
        report = f"""分类结果：
类别：{category}
{description}

分析：
这首诗的写作风格和内容特点符合{category}的特征。
"""
        
        return category, report
    except Exception as e:
        print(f"分类过程中出现错误：{str(e)}")
        return "未知", f"分类失败：{str(e)}"

if __name__ == "__main__":
    # 测试
    test_poem = """春眠不觉晓
处处闻啼鸟
夜来风雨声
花落知多少"""
    
    category, report = classify_poem(test_poem)
    print(report) 