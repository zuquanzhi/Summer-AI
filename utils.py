# utils.py
import time
import os
import simpleaudio as sa
from config import PROMPT_SOUND_FILE

# 全局变量：记录最后一次交互时间
last_interaction = time.time()

def update_last_interaction():
    """更新最后一次交互时间为当前时间"""
    global last_interaction
    last_interaction = time.time()

def get_last_interaction():
    """返回最后一次交互时间"""
    return last_interaction

def play_prompt_sound():
    """
    播放提示音文件，用于提示用户状态变化。
    注意：确保 PROMPT_SOUND_FILE 文件存在且为有效的 wav 格式音频文件。
    """
    if os.path.exists(PROMPT_SOUND_FILE):
        try:
            wave_obj = sa.WaveObject.from_wave_file(PROMPT_SOUND_FILE)
            play_obj = wave_obj.play()
            play_obj.wait_done()
            update_last_interaction()  # 在提示音播放结束后更新交互时间
        except Exception as e:
            print(f"提示音播放失败: {e}")
    else:
        print("提示音文件不存在")
        
def play_hello_sound():
    """
    播放欢迎音文件，用于提示用户状态变化。
    注意：确保 hello.wav 和 home.wav 文件存在且为有效的 wav 格式音频文件。
    """
    files_to_play = ["hellotest.wav", "home.wav"]
    
    for file in files_to_play:
        if os.path.exists(file):
            try:
                wave_obj = sa.WaveObject.from_wave_file(file)
                play_obj = wave_obj.play()
                play_obj.wait_done()
                update_last_interaction()  # 在提示音播放结束后更新交互时间
            except Exception as e:
                print(f"提示音播放失败: {e}")
        else:
            print(f"提示音文件 {file} 不存在")
