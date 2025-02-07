
import azure.cognitiveservices.speech as speechsdk
from config import WAKE_WORD_MODEL_FILE
from utils import update_last_interaction, play_prompt_sound, play_hello_sound
import time
import threading
from azure_speech import init_stt


# 全局初始化唤醒词模型和关键词识别器
def init_keyword_recognizer():
    """初始化关键词识别器和唤醒词模型"""
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    keyword_recognizer = speechsdk.KeywordRecognizer(audio_config)
    try:
        keyword_model = speechsdk.KeywordRecognitionModel(WAKE_WORD_MODEL_FILE)
    except Exception as e:
        print(f"加载唤醒词模型失败: {e}")
        return None, None
    return keyword_recognizer, keyword_model

# 唤醒词监听线程
def listen_for_keyword(keyword_recognizer, keyword_model, stop_event):
    """监听唤醒词，检测到唤醒词时退出"""
    while not stop_event.is_set():
        print("等待唤醒词...")
        welcome_thread = threading.Thread(target=play_hello_sound)
        result_future = keyword_recognizer.recognize_once_async(keyword_model)  # 使用recognize_once_async方法
        result = result_future.get()  # 获取结果

        if result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print("系统已唤醒，恢复交互")
            stop_event.set()
            welcome_thread.start()
            return


        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("未检测到唤醒词，请重试")
        elif result.reason == speechsdk.ResultReason.Canceled:
            print("唤醒词识别被取消")



def sleep_mode(speech_config, synthesizer):
    """
    休眠模式：利用 Azure 关键词识别功能检测唤醒词，一旦检测到唤醒词则退出休眠状态
    """
    print("系统进入休眠模式，等待唤醒指令...")
    # update_last_interaction()  # 更新交互时间
    play_prompt_sound()  # 播放提示音提示进入休眠

    # 初始化关键词识别器和唤醒词模型
    keyword_recognizer, keyword_model = init_keyword_recognizer()
    if not keyword_recognizer or not keyword_model:
        return

    # 创建停止事件
    stop_event = threading.Event()
    # recognizer = init_stt(speech_config)


    # 启动唤醒词监听线程
    wake_thread = threading.Thread(target=listen_for_keyword, args=(keyword_recognizer, keyword_model, stop_event))
    wake_thread.daemon = True
    wake_thread.start()

    # 等待唤醒线程结束
    wake_thread.join()