import json
import sys
from draw_Rect import TransparentDrawingWidget
import speech_recognition as sr
import pyttsx3
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QRect
from LLM_tools import LLMClient
from get_position import click_position,get_position


def listen_for_keyword(recognizer, microphone):
    def formulateResult(resu):
        start = resu.index('"', resu.index('"', resu.index('"') + 1) + 1) + 1
        end = resu.index('"', start)
        return resu[start:end]
    while True:
        with microphone as source:
            audio = recognizer.listen(source)
        try:
            # speech = recognizer.recognize_google(audio, language='zh-CN')
            speech = recognizer.recognize_vosk(audio)
            speech = formulateResult(speech)
            speech = speech.replace(" ","")
            print("用户："+ speech)
            return speech
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Could not request results; {e}")


if __name__ == '__main__':
    client = LLMClient()
    engine = pyttsx3.init()  # 创建engine并初始化
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    app = QApplication(sys.argv)
    widget = TransparentDrawingWidget()

    while True:
        prompt = listen_for_keyword(recognizer, microphone)
        if prompt == "":
            continue
        # 第三步，发起交互
        message = [
            {'role': 'user', 'content': prompt}
        ]
        ops = client.ask(message)[0].get('function_call').get('arguments')
        engine.say("收到")  # 开始朗读
        engine.runAndWait()  # 等待语音播报完毕
        ops = json.loads(ops)
        watch_element = ops.get('watch', ["没有该元素"])
        click_element = ops.get('click', ["没有该元素"])
        setting_element = ops.get('settings', ["没有该元素"])
        draw_element = ops.get('draw', ["没有该元素"])
        if watch_element != ["没有该元素"]:
            # print(watch_element[0].strip("播放"))
            click_position(watch_element[0].strip("播放"))
            continue
        if click_element != ["没有该元素"]:
            # print(click_element[0].strip("点击"))
            click_position(click_element[0].strip("点击"))
            continue
        # if setting_element != ["没有该元素"]:
        #     print(setting_element[0].strip("点击"))
        #     get_position(setting_element[0].strip("点击"))
        #     continue
        if draw_element != ["没有该元素"]:
            # print(draw_element[0].strip("绘制"))

            top_left_arr, bottom_right_arr = get_position(draw_element[0].strip("绘制").strip("框选"))
            for index, item in enumerate(top_left_arr):
                # 计算需要的值
                top_left_x = top_left_arr[index][0]
                top_left_y = top_left_arr[index][1]
                bottom_right_x = bottom_right_arr[index][0]
                bottom_right_y = bottom_right_arr[index][1]

                width = bottom_right_x - top_left_x
                height = bottom_right_y - top_left_y
                # print(top_left_x, top_left_y, width, height)
                # 示例：绘制一个矩形框
                if index == 0:
                    widget.draw(top_left_x, top_left_y, width, height)
                # 示例：你可以通过调用 `widget.clear()` 来清除绘制内容
            widget.show()
    sys.exit(app.exec())

'''
docker pull registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.10 

本地电脑： mkdir -p ./funasr-runtime-resources/models  

docker save -o funasr.tar 1c2adfcff84df11cac2f5c20aa4bc62c521fa7f269f5e44848fd55cc973023b1

docker tag 1c2adfcff84df11cac2f5c20aa4bc62c521fa7f269f5e44848fd55cc973023b1 funasr_cpu:funasr_diy

docker run -p 10096:10095 -itd --privileged=true -v D:/PycharmProjects/Image-element-positioning/funasr-runtime-resources/models:/workspace/models funasr_cpu:funasr_diy

docker attach f99d74b72307c69bc4233400fa8aebcd422e8bdbaf686c33dbb981b5134fe7ba

# 启动服务
bash run_server_2pass.sh

ws://127.0.0.1:10096/
'''