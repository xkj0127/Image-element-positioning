import json
import os
import threading
import time
import requests
import re
import speech_recognition as sr
import pyttsx3




class GongZhu:
    def __init__(self,model="qwen2",type="你是一个中国美女，回答以聊天的口头语为主，喜欢和我分享你所知道的任何东西，你的回答必须中文"):
        super().__init__()
        self.type = type
        self.model = model
        self.host = "127.0.0.1"
        self.port = "11434"
        self.engine = pyttsx3.init()  # 创建engine并初始化
        self.message = [
                {"role": "system", "content": self.type},
                
            ]

    def typewriter_effect(self, text):
        print("AI:")
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.07)  # 控制打字机效果的速度
        print()  # 打印换行

    def chat_stream(self, prompt):
        prompt = prompt.replace(" ", "")
        print("用户:"+prompt)
        data = {
            "model": self.model,
            "messages": self.message,
            "stream":False
        }
        self.message.append({"role": "user", "content": prompt})
        # 发送带有流式响应的 POST 请求
        with requests.post("http://" + self.host + ":" + self.port + "/api/chat", json=data, stream=False) as response:

            text = re.findall(r'"content":"(.*?)"', response.text)
            text = text[0].replace("\\n", "")
            text = text.replace("!", "")
            text = text.replace("！", "")
            
            # print(text)
            self.message.append({"role": "assistant", "content": text})
            threading.Thread(target=self.typewriter_effect, args=(text,)).start()  # 启动打字机效果的线程
            self.engine.say(text)  # 开始朗读
            self.engine.runAndWait()  # 等待语音播报完毕

   
    def formulateResult(self,resu):
        start = resu.index('"', resu.index('"', resu.index('"') + 1) + 1) + 1
        end = resu.index('"', start)
        return resu[start:end]


    def listen_for_keyword(self,recognizer, microphone):
        while True:
            with microphone as source:
                audio = recognizer.listen(source)
            try:
                #speech = recognizer.recognize_google(audio, language='zh-CN')
                speech = recognizer.recognize_vosk(audio)
                speech=self.formulateResult(speech)

                return speech
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("Could not request results; {e}")


if __name__ == '__main__':
    
    gongzhu = GongZhu()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    while True:

        prompt = gongzhu.listen_for_keyword(recognizer, microphone)
        if prompt :
            gongzhu.chat_stream(prompt)