import time
import cv2
# import easyocr
import warnings
import pyautogui
import time
import cv2
import pyautogui
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import sys
warnings.filterwarnings("ignore")

# reader = easyocr.Reader(['ch_sim'], gpu=True)


# FIXME： 用于测试ORC的识别时间
# 定义装饰器
def time_calc(func):
    def wrapper(*args, **kargs):
        start_time = time.time()
        f = func(*args, **kargs)
        exec_time = time.time() - start_time
        print("func.name:{}\texec_time:{}".format(func.__name__, exec_time))
        return f

    return wrapper


# @time_calc
# def click_position(element, index=1):
#     boxxy = 0
#     count_text = 0
#
#     # 截取屏幕截图
#     screenshot = pyautogui.screenshot()
#
#     # screenshot.save('screenshot.png')
#     # 将PIL图像转换为NumPy数组
#     image_np = np.array(screenshot)
#
#     # OpenCV使用的BGR格式
#     image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
#
#     # 创建EasyOCR阅读器（指定中文和英文）
#
#     # 进行OCR检测
#     results = reader.readtext(image_np)
#
#     # 查找特定字符的位置
#     target_char = element
#
#     # 得到当前页面需要点击元素的个数，如果大于1则需要绘制图框
#     for (bbox, text, prob) in results:
#         if target_char in text:
#             count_text += 1
#             boxxy = bbox
#             break
#
#     # TODO: 还没考虑当前窗口具有两个相同元素的时候的决策：1.增加pyside6进行元素框选让用户选择需要点击的具体元素 2.选择后清除绘制 3.无结果提示
#     match count_text:
#         case 0:
#             # 提示用户当前页面无该元素
#             pass
#         case 1:
#             # 点击该元素
#             (top_left, top_right, bottom_right, bottom_left) = boxxy
#             top_left = tuple(map(int, top_left))
#             bottom_right = tuple(map(int, bottom_right))
#             # 在图像上绘制矩形框以标记字符位置
#             cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 2)
#             print(f'Character "{target_char}" found at: top_left={top_left}, bottom_right={bottom_right}')
#             target_x = int((top_left[0] + bottom_right[0]) / 2)
#             target_y = int((top_left[1] + bottom_right[1]) / 2)
#             # print(target_x, target_y)
#             pyautogui.click(target_x, target_y)  # 左击坐标(100,150)
#
#
# @time_calc
# def get_position(element):
#     top_left_arr = []
#     bottom_right_arr = []
#     # 截取屏幕截图
#     screenshot = pyautogui.screenshot()
#
#     # 将PIL图像转换为NumPy数组
#     image_np = np.array(screenshot)
#
#     # OpenCV使用的BGR格式
#     image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
#
#     # 创建EasyOCR阅读器（指定中文和英文）
#     reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)
#
#     # 进行OCR检测
#     results = reader.readtext(image_np)
#
#     # 查找特定字符的位置
#     target_char = element
#
#     # 得到当前页面需要点击元素的个数，如果大于1则需要绘制图框
#     for (bbox, text, prob) in results:
#         if target_char in text:
#             (top_left, top_right, bottom_right, bottom_left) = bbox
#             top_left = tuple(map(int, top_left))
#             bottom_right = tuple(map(int, bottom_right))
#             # 在图像上绘制矩形框以标记字符位置
#             cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 2)
#             print(f'Character "{target_char}" found at: top_left={top_left}, bottom_right={bottom_right}')
#             top_left_arr.append(top_left)
#             bottom_right_arr.append(bottom_right)
#
#     return top_left_arr, bottom_right_arr

ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)

@time_calc
def click_position(key):
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    text = ocr.ocr("screenshot.png",cls=True)
    # print(text)
    for i in text[0]:
        # print(i[1][0])
        if key in i[1][0]:
            print(i)
            position = i[0]
            # 顺时针
            (top_left, top_right, bottom_right, bottom_left) = position

            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))

            print(f'Character "{i[1][0]}" found at: top_left={top_left}, bottom_right={bottom_right}')
            target_x = int((top_left[0] + bottom_right[0]) / 2)
            target_y = int((top_left[1] + bottom_right[1]) / 2)
            # print(target_x, target_y)
            pyautogui.click(target_x, target_y)  # 左击坐标(100,150)
            return 0


def move_position(type):
    if type == '往下一点':
        pyautogui.scroll(-300)
    elif type == '往上一点':
        pyautogui.scroll(300)


if __name__ == '__main__':
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)
    click_position("热门")
    # top_left_arr, bottom_right_arr=get_position("见证历史")
    # app = QApplication(sys.argv)
    # widget = TransparentDrawingWidget()
    # for index,item in enumerate(top_left_arr):
    #     # 计算需要的值
    #     top_left_x = top_left_arr[index][0]
    #     top_left_y = top_left_arr[index][1]
    #     bottom_right_x = bottom_right_arr[index][0]
    #     bottom_right_y = bottom_right_arr[index][1]
    #
    #     width = bottom_right_x - top_left_x
    #     height = bottom_right_y - top_left_y
    #     print(top_left_x, top_left_y, width, height)
    #     # 示例：绘制一个矩形框
    #     widget.draw(top_left_x,top_left_y,width,height)
    #     print("draw")
    #     widget.show()
    #     # 示例：你可以通过调用 `widget.clear()` 来清除绘制内容
    # sys.exit(app.exec())
