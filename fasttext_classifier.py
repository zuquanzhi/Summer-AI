# fasttext_classifier.py
import random
import fasttext

def generate_training_data(filename="intent_classification.txt", n_samples=1000):
    """
    自动生成训练数据文件。
    
    参数：
      - filename：保存训练数据的文件名
      - n_samples：每个类别生成的样本数（任务和聊天各 n_samples 条）
    
    生成格式如下：
      __label__task    播放音乐
      __label__chat    你今天怎么样？
    """
    # 任务类示例短语
    task_phrases = [
        "播放音乐", "请播放一首歌", "帮我放点音乐", "我要听音乐", "播放一下歌曲",
        "关灯", "请把灯关掉", "把房间灯关了", "灯，请关掉", "请关闭灯光",
        "查询天气", "请告诉我天气", "天气怎么样", "查询今天的温度", "查一下气温",
        "调高音量", "请把音量调大", "增大音量", "提高声音", "请调高声音",
        "调低音量", "请把音量调低", "降低音量", "减小声音", "请调低声音"
    ]
    
    # 聊天类示例短语
    chat_phrases = [
        "你今天怎么样", "你好", "最近如何", "讲个笑话", "天气真好", "你觉得如何",
        "我该怎么办", "生活真有趣", "你喜欢什么", "我们聊点别的", "今天心情不错",
        "聊聊天吧", "给我讲个故事", "你的观点是什么", "我想知道更多"
    ]
    
    with open(filename, "w", encoding="utf-8") as f:
        # 生成任务指令样本
        for _ in range(n_samples):
            phrase = random.choice(task_phrases)
            f.write(f"__label__task\t{phrase}\n")
        # 生成聊天样本
        for _ in range(n_samples):
            phrase = random.choice(chat_phrases)
            f.write(f"__label__chat\t{phrase}\n")
    
    print(f"生成训练数据 {filename} 完成，共计 {2 * n_samples} 条样本。")

if __name__ == "__main__":
    # 生成足够大的训练数据集（这里每个类别 1000 条，共 2000 条数据）
    # generate_training_data(filename="intent_classification.txt", n_samples=1000)
    
    # 训练 FastText 模型
    # 这里我们设定 epoch=25、学习率 lr=1.0、2-gram 特征，参数可根据实际情况调整
    model = fasttext.train_supervised(
        input="intent_classification.txt",
        epoch=25,
        lr=1.0,
        wordNgrams=2,
        verbose=2
    )
    
    # 保存训练好的模型
    model.save_model("intent_classification.bin")
    print("FastText 模型训练完成，并保存为 intent_classification.bin")
