"""
生成模型配置
"""

class GeneratorConfig:
    # 模型参数
    model_name = "uer/gpt2-chinese-cluecorpussmall"  # 使用中文GPT-2模型
    max_length = 32  # 五言绝句通常不超过32个token
    batch_size = 8
    learning_rate = 5e-5
    num_epochs = 20
    
    # 数据路径
    train_data_path = "data/poem_generation_processed.csv"
    model_save_path = "models/generator"
    
    # 训练参数
    train_test_split = 0.1  # 使用90%的数据进行训练
    random_seed = 42
    
    # 设备配置
    device = "cuda"  # 如果没有GPU，会自动切换到CPU 