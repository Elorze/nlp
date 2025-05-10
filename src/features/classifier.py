from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os
from config.classifier_config import ClassifierConfig

class PoetryClassifier:
    def __init__(self):
        self.config = ClassifierConfig()
        self.device = torch.device(self.config.device if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        try:
            # 初始化tokenizer和模型
            print("Loading tokenizer...")
            self.tokenizer = BertTokenizer.from_pretrained(self.config.model_name)
            
            print("Loading model...")
            self.model = BertForSequenceClassification.from_pretrained(
                self.config.model_name,
                num_labels=self.config.num_labels
            ).to(self.device)
            
            # 如果模型已经训练好，加载模型
            model_path = os.path.join(self.config.model_save_path, "pytorch_model.bin")
            if os.path.exists(model_path):
                print(f"Loading trained model from {model_path}...")
                self.model.load_state_dict(
                    torch.load(model_path, map_location=self.device)
                )
            else:
                print(f"Warning: Model file not found at {model_path}")
            
            self.label_reverse_map = {v: k for k, v in self.config.label_map.items()}
            print("Classifier initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing classifier: {str(e)}")
            raise
    
    def classify(self, text):
        """对单个诗词进行分类"""
        try:
            self.model.eval()
            
            # 预处理文本
            inputs = self.tokenizer(
                text,
                add_special_tokens=True,
                max_length=self.config.max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            # 将输入移到正确的设备上
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # 进行预测
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.argmax(outputs.logits, dim=1)
                predicted_label = predictions.item()
            
            return self.label_reverse_map[predicted_label]
            
        except Exception as e:
            print(f"Error in classification: {str(e)}")
            return "未知"
    
    def batch_classify(self, texts):
        """对多个诗词进行批量分类"""
        try:
            self.model.eval()
            
            # 预处理文本
            inputs = self.tokenizer(
                texts,
                add_special_tokens=True,
                max_length=self.config.max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            # 将输入移到正确的设备上
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # 进行预测
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.argmax(outputs.logits, dim=1)
            
            # 将预测结果转换为类别标签
            return [self.label_reverse_map[pred.item()] for pred in predictions]
            
        except Exception as e:
            print(f"Error in batch classification: {str(e)}")
            return ["未知"] * len(texts)
    
    def train(self, train_data, labels):
        # 训练模型的代码将在后续实现
        pass 