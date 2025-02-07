# azure_speech.py
import azure.cognitiveservices.speech as speechsdk
from config import AZURE_SPEECH_KEY, AZURE_REGION
import time
from utils import play_prompt_sound

def init_speech_config():
    """
    初始化 Azure 语音服务配置
    """
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
    speech_config.speech_recognition_language = "zh-CN"
    # 延长初始静默超时到 10 秒
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "10000")
    return speech_config

def init_tts():
    """
    初始化语音合成（TTS）并配置语音风格
    """
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
    # 设置语音风格为 zh-CN-XiaoxiaoNeural（女性语音）
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
    
    ssml = """
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
        <voice name='zh-CN-XiaoxiaoNeural'>
            <prosody rate='1.0' pitch='0.0'>
                欢迎使用语音交互系统
            </prosody>
        </voice>
    </speak>
    """
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    return synthesizer, ssml

def init_stt(speech_config):
    """
    初始化语音识别（STT）
    """
    return speechsdk.SpeechRecognizer(speech_config=speech_config)

def speech_to_text(recognizer):
    """
    调用 Azure 的语音识别接口，并返回识别结果
    """
    print("\n请开始说话...")
    play_prompt_sound()
    # print("当前时间戳为：", time.time())
    
    result = recognizer.recognize_once()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"识别结果: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("语音不清晰，请重试")
        return None
    else:
        print("系统识别错误")
        return None
