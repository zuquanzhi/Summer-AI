# config.py
# 注意：实际项目中不要将秘钥硬编码在代码中，可以使用环境变量或配置文件来管理

AZURE_SPEECH_KEY = ""
AZURE_REGION = "eastus"

DEEPSEEK_API_KEY = ""

# 休眠超时时间（秒）
SLEEP_TIMEOUT = 5

# 唤醒词关键词模型文件（确保文件存在且为 Azure 生成的唤醒词模型文件）
WAKE_WORD_MODEL_FILE = "Summer.table"

# 提示音文件（确保文件存在且为有效的 wav 格式音频文件）
PROMPT_SOUND_FILE = "test.wav"

# FastText 模型文件路径
FASTTEXT_MODEL_PATH = "intent_classification.bin"

# 大模型配置（以支持多种大模型）
MODEL_CONFIGS = {
    "deepseek": {
        "api_key": DEEPSEEK_API_KEY,
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat"  # DeepSeek模型的名称
    },
    "openai": {
        "api_key": "your-openai-api-key",  # 用你自己的 API 密钥替代
        "base_url": "https://api.openai.com/v1",  # 如果你使用的是 OpenAI GPT API
        "model": "gpt-3.5-turbo"  # OpenAI 模型名称
    },

    "tongyi": {
        "api_key": "sk-151dcba46f6c4825a28bd9e8d106abdf",  # 用你自己的 API 密钥替代
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",  # 如果你使用的是 Tongyi API
        "model": "qwen-plus"  # Tongyi 模型名称
    }
}

# 默认选择的模型
DEFAULT_MODEL = "tongyi"