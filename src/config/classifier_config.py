"""
分类器配置
"""

class ClassifierConfig:
    # 模型参数
    model_name = "bert-base-chinese"
    num_labels = 3
    max_length = 128
    batch_size = 16
    learning_rate = 2e-5
    num_epochs = 10
    
    # 数据路径
    train_data_path = "data/poem_classification_processed.csv"
    model_save_path = "models/classifier"
    
    # 训练参数
    train_test_split = 0.2
    random_seed = 42
    
    # 标签映射
    label_map = {
        "山水": 0,
        "咏史": 1,
        "送别": 2
    }
    
    # 设备配置
    device = "cuda"  # 如果没有GPU，会自动切换到CPU 