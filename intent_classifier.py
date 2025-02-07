# intent_classifier.py
import fasttext
from config import FASTTEXT_MODEL_PATH

FASTTEXT_MODEL_PATH = "/Users/zuquanzhi/Programs/Summer/project/intent_classification.bin"
# 加载预训练的 FastText 模型
model = fasttext.load_model(FASTTEXT_MODEL_PATH)

# 定义任务指令分类函数
def classify_intent(text):
    """
    使用 FastText 模型判断输入是否为任务指令。
    返回 True 表示为任务指令，否则为聊天。
    """
    # 预测标签
    label = model.predict(text)[0][0]
    return label == "__label__task" 
    
## 测试
print(classify_intent("你是谁"))  # False