import json
import sys
from PySide6.QtCore import QTimer
from draw_Rect import TransparentDrawingWidget
import speech_recognition as sr
import pyttsx3
from PySide6.QtWidgets import QApplication
from LLM_tools import LLMClient
from get_position import click_position, get_position

def listen_for_keyword(recognizer, microphone):
    while True:
        with microphone as source:
            audio = recognizer.listen(source)
        try:
            speech = recognizer.recognize_google(audio, language='zh-CN')
            print(f"用户: {speech}")
            return speech
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

def process_input():
    prompt = input("请输入")  # For testing, replace with listen_for_keyword in production
    # prompt = listen_for_keyword(recognizer, microphone)
    message = [{'role': 'user', 'content': prompt}]
    ops = client.ask(message)[0].get('function_call').get('arguments')
    engine.say("收到")
    engine.runAndWait()
    ops = json.loads(ops)
    watch_element = ops.get('watch', ["没有该元素"])
    click_element = ops.get('click', ["没有该元素"])
    setting_element = ops.get('settings', ["没有该元素"])
    draw_element = ops.get('draw', ["没有该元素"])
    clean_element = ops.get('clean', ["没有该元素"])

    if watch_element != ["没有该元素"]:
        print(watch_element[0].strip("播放"))
        click_position(watch_element[0].strip("播放"))
    elif click_element != ["没有该元素"]:
        print(click_element[0].strip("点击"))
        click_position(click_element[0].strip("点击"))
    elif clean_element != ["没有该元素"]:
        widget.clear()
    elif draw_element != ["没有该元素"]:
        print(draw_element[0].strip("绘制"))
        top_left_arr, bottom_right_arr = get_position(draw_element[0].strip("绘制").strip('框选'))
        for index, item in enumerate(top_left_arr):
            top_left_x = top_left_arr[index][0]
            top_left_y = top_left_arr[index][1]
            bottom_right_x = bottom_right_arr[index][0]
            bottom_right_y = bottom_right_arr[index][1]
            width = bottom_right_x - top_left_x
            height = bottom_right_y - top_left_y
            print(top_left_x, top_left_y, width, height)
            widget.draw(top_left_x, top_left_y, width, height)

# 喜羊羊
if __name__ == '__main__':
    client = LLMClient()
    engine = pyttsx3.init()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    app = QApplication(sys.argv)
    widget = TransparentDrawingWidget()

    # Set up a QTimer to periodically process input
    timer = QTimer()
    timer.timeout.connect(process_input)
    timer.start(5000)  # Adjust the interval as needed (in milliseconds)

    widget.show()
    sys.exit(app.exec())
