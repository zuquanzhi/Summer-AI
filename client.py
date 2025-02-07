import time
import requests
from config import MODEL_CONFIGS, DEFAULT_MODEL
from utils import play_prompt_sound

def get_chat_response(client, user_input):
    """
    调用对应的大模型 API 获取聊天回答，具有错误重试机制
    """
    model_config = MODEL_CONFIGS.get(DEFAULT_MODEL)  # 获取配置文件中指定的模型配置
    if not model_config:
        return "配置文件错误，未找到相应的模型"

    retry_count = 0
    while retry_count < 3:
        try:
            if DEFAULT_MODEL == "deepseek":
                # 使用 DeepSeek API
                response = client.chat.completions.create(
                    model=model_config["model"],
                    messages=[
                        {"role": "system", "content": "你是由全之开发的的超级智能助手Summer，具备全面而强大的知识储备、快速高效的响应能力和深度问题分析能力，无论科技、生活还是娱乐领域的疑问，都能迅速提供简洁凝练、准确且富有洞察力的答案，并在必要时主动询问细节以确保理解正确，同时始终保持专业、友好与礼貌的沟通风格，为用户提供既解决问题又启发思考的实用建议。回答要简洁专业"},
                        {"role": "user", "content": user_input},
                    ],
                    stream=False
                )
            elif DEFAULT_MODEL == "openai":
                # 使用 OpenAI API
                headers = {
                    "Authorization": f"Bearer {model_config['api_key']}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": model_config["model"],
                    "messages": [
                        {"role": "system", "content": "你是由全之开发的的超级智能助手Summer，具备全面而强大的知识储备、快速高效的响应能力和深度问题分析能力，无论科技、生活还是娱乐领域的疑问，都能迅速提供简洁凝练、准确且富有洞察力的答案，并在必要时主动询问细节以确保理解正确，同时始终保持专业、友好与礼貌的沟通风格，为用户提供既解决问题又启发思考的实用建议。回答要简洁专业"},
                        {"role": "user", "content": user_input},
                    ]
                }
                response = requests.post(f"{model_config['base_url']}/chat/completions", headers=headers, json=data)
                response = response.json()
            elif DEFAULT_MODEL == "tongyi":
                # 使用 TongYiQianWen API
                headers = {
                    "Authorization": f"Bearer {model_config['api_key']}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": model_config["model"],
                    "messages": [
                        {"role": "system", "content": "你是由全之开发的的超级智能助手Summer，具备全面而强大的知识储备、快速高效的响应能力和深度问题分析能力，无论科技、生活还是娱乐领域的疑问，都能迅速提供简洁凝练、准确且富有洞察力的答案，并在必要时主动询问细节以确保理解正确，同时始终保持专业、友好与礼貌的沟通风格，为用户提供既解决问题又启发思考的实用建议。回答要简洁专业"},
                        {"role": "user", "content": user_input},
                    ]
                }
                response = requests.post(f"{model_config['base_url']}/chat/completions", headers=headers, json=data)
                response = response.json()

            # 成功获取到回答后，播放提示音并返回结果
            play_prompt_sound()  # 表示系统已生成回答
            return response["choices"][0]["message"]["content"]
        
        except Exception as e:
            print(f"API错误: {str(e)}，重试中...")
            retry_count += 1
            time.sleep(1)

    return "服务暂时不可用，请稍后再试"
