
import time
from azure_speech import init_speech_config, init_tts, init_stt, speech_to_text
from client import get_chat_response
from wakeup import sleep_mode
from utils import update_last_interaction, play_prompt_sound, get_last_interaction,play_hello_sound
from openai import OpenAI
from config import SLEEP_TIMEOUT, MODEL_CONFIGS, DEFAULT_MODEL
from task_handler import TaskClassifier, TaskExecutor

def main():
    # 初始化任务分类器和执行器
    task_classifier = TaskClassifier()
    task_executor = TaskExecutor()
    
    # 初始化语音合成（TTS）
    synthesizer, ssml = init_tts()
    synthesizer.speak_ssml(ssml)
    update_last_interaction()

    # 从 config.py 获取当前大模型配置
    model_config = MODEL_CONFIGS.get(DEFAULT_MODEL)
    if not model_config:
        print("配置错误，未找到指定的大模型")
        return

    # 初始化 DeepSeek 客户端（聊天部分）或其他模型的客户端
    if DEFAULT_MODEL == "deepseek":
        client = OpenAI(api_key=model_config["api_key"], base_url=model_config["base_url"])
    elif DEFAULT_MODEL == "openai":
        client = OpenAI(api_key=model_config["api_key"], base_url=model_config["base_url"])
    elif DEFAULT_MODEL == "tongyi":
        client = OpenAI(api_key=model_config["api_key"], base_url=model_config["base_url"])
    else:
        print("未配置支持的模型类型")
        return

    failure_count = 0
    speech_config = init_speech_config()  # 初始化语音配置
    recognizer = init_stt(speech_config)  # 初始化语音识别器，只需初始化一次
    
    # 进入休眠模式，等待唤醒指令
    sleep_mode(speech_config, synthesizer)
    # play_hello_sound()

    update_last_interaction()

    while True:
        recognizer = init_stt(speech_config)       
        # 每次进入语音识别前检查是否需要进入休眠模式
        if time.time() - get_last_interaction() > SLEEP_TIMEOUT:
            sleep_mode(speech_config, synthesizer)
            play_hello_sound()
            update_last_interaction()
            failure_count = 0  # 重置失败计数
            continue

        # 进行语音识别，获取用户输入
        user_input = speech_to_text(recognizer)
        update_last_interaction()

        # 如果没有有效识别结果，提示用户重新说一遍
        if not user_input:
            failure_count += 1
            if failure_count >= 2:
                update_last_interaction()
                play_prompt_sound()
                sleep_mode(speech_config, synthesizer)
                update_last_interaction()
                failure_count = 0  # 重置失败计数
                continue
            else:
                synthesizer.speak_text("抱歉没听清，请您重新说一遍")
                update_last_interaction()
                play_prompt_sound()
                continue
        else:
            failure_count = 0  # 重置失败计数
            update_last_interaction()

        # 先进行任务分类（基于关键字匹配）
        task = task_classifier.classify(user_input)
        if task:
            print(f"检测到任务指令：{task}")
            task_executor.execute(task,user_input)
            continue  # 执行完任务后跳过聊天流程

        print("未检测到任务指令，进入聊天模式...")

        # 获取 AI 回答（聊天流程）
        print("生成回答中...")
        response = get_chat_response(client, user_input)

        # 语音合成回答
        if response:
            print(f"AI回复：{response}")
            synthesizer.speak_text(response)
            update_last_interaction()
        else:
            synthesizer.speak_text("这个问题我需要再想想")
            update_last_interaction()
            play_prompt_sound()

if __name__ == "__main__":
    main()