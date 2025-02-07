import requests
from duckduckgo_search import DDGS
from pprint import pprint
# from azure_speech import SpeechSynthesizer
from azure_speech import init_tts
from config import AZURE_SPEECH_KEY, AZURE_REGION
import time
from utils import update_last_interaction, play_prompt_sound, get_last_interaction,play_hello_sound



class TaskClassifier:
    """
    任务分类器：根据输入文本中的关键字判断是否为任务指令，
    并返回相应的任务标识符，如果没有检测到任务关键字，则返回 None。
    """
    def __init__(self):
        
        # 定义任务与关键字的映射，关键字可以是多个模糊匹配词
        self.task_keywords = {
            "play_music": ["音乐", "听歌", "放歌"],
            "query_weather": ["天气", "温度", "气候"],
            "control_light": ["灯", "开灯", "关灯"],
            "increase_volume": ["调高", "增大音量"],
            "decrease_volume": ["调低", "减小音量"],
            "search": ["搜索", "查找", "查询", "今天的新闻", "最新新闻"],  # 扩展搜索关键字
            "time": ["时间", "几点了", "现在几点"]
        }

    def classify(self, text: str) -> str:
        """
        遍历所有任务关键字，如果在输入文本中匹配到任一关键字，
        则返回对应任务类型，否则返回 None 表示未检测到任务指令。
        """
        for task, keywords in self.task_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return task
        return None  # 未识别为任务


class TaskExecutor:
    """
    任务执行器：根据任务标识符执行相应的操作。
    在实际项目中，这里的每个方法都可以扩展为调用具体的 API 或控制设备等动作。
    """
    def __init__(self):
        self.synthesizer, self.ssml = init_tts()

    def execute(self, task: str, user_input: str):
        if task == "play_music":
            self.play_music()
        elif task == "query_weather":
            self.query_weather()
        elif task == "control_light":
            self.control_light()
        elif task == "increase_volume":
            self.increase_volume()
        elif task == "decrease_volume":
            self.decrease_volume()
        elif task == "search":
            self.search(user_input)
        elif task == "time":
            self.synthesizer.speak_text(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            
        else:
            print("未知任务类型，无法执行。")
        update_last_interaction()

    def play_music(self):
        print("【任务执行】正在播放音乐...")
        # 这里可以加入实际播放音乐的代码

    def query_weather(self):
        print("【任务执行】正在查询天气...")
        # 这里可以加入实际查询天气的代码

    def control_light(self):
        print("【任务执行】正在控制灯光状态...")
        # 这里可以加入实际控制灯光的代码

    def increase_volume(self):
        print("【任务执行】正在调高音量...")
        # 执行调高音量的代码

    def decrease_volume(self):
        print("【任务执行】正在调低音量...")
        # 这里可以加入实际调低音量的代码

    def search(self, query: str):
        """
        根据用户的搜索请求，调用 DuckDuckGo 搜索引擎 API 进行搜索
        """
        print(f"【任务执行】正在搜索：{query}")
        result = self.ddgs_search(query)
        
        # 如果有结果，将其通过语音播报
        if result:
            self.speak_search_results(result)
        else:
            self.synthesizer.speak_text("抱歉，未能找到相关信息。")

    # 使用 DDGS (DuckDuckGo Search) 进行搜索
    def ddgs_search(self, query: str):
        with DDGS() as ddgs:
            # 搜索结果可以通过`ddgs.text()`获取，并限制结果数量（例如 max_results=5）
            search_results = [r for r in ddgs.text(query, region='cn-zh', max_results=1)]
            
            # 整理搜索结果，提取摘要
            cleaned_results = []
            for result in search_results:
                cleaned_results.append(result['body'])  # 仅返回摘要内容（不包括URL）
                print(f"标题：{result['body']}")
                self.synthesizer.speak_text(result['body'])  # 语音播报搜索结果
            
            return cleaned_results

    def speak_search_results(self, results):
        for result in results:
            self.synthesizer.speak_text(result)