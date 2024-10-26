import sys
import asyncio
import websockets
import json
import logging
import pyaudio
from PySide6 import QtWidgets
from qasync import QEventLoop, asyncSlot

# 日志配置
logging.basicConfig(level=logging.ERROR)


class SpeechRecognitionClient(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.websocket = None
        self.offline_msg_done = False  # 识别完成标志

    def initUI(self):
        self.setWindowTitle("实时语音识别")
        self.setGeometry(100, 100, 400, 300)

        # 创建按钮
        self.start_button = QtWidgets.QPushButton("开始识别", self)
        self.start_button.clicked.connect(self.start_recognition)

        self.stop_button = QtWidgets.QPushButton("停止识别", self)
        self.stop_button.clicked.connect(self.stop_recognition)

        # 创建文本框
        self.result_text = QtWidgets.QTextEdit(self)
        self.result_text.setReadOnly(True)

        # 设置布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.result_text)
        self.setLayout(layout)

    async def connect_websocket(self):
        """连接到WebSocket服务端"""
        try:
            self.websocket = await websockets.connect("ws://localhost:10096")
            logging.info("连接到服务端")
        except Exception as e:
            logging.error("连接到WebSocket服务端失败: %s", e)
            self.result_text.append("连接到服务端失败")

    async def record_microphone(self):
        """从麦克风录音并将数据发送到WebSocket服务端"""
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=960)

        message = json.dumps({
            "mode": 'offline',
            "chunk_size": [5, 10, 5],
            "chunk_interval": 10,
            "wav_name": "microphone",
            "is_speaking": True,
            "hotwords": '',
            "itn": False
        })

        if self.websocket is not None:
            await self.websocket.send(message)
        else:
            logging.error("WebSocket连接未建立")
            return

        try:
            while not self.offline_msg_done:
                data = stream.read(960, exception_on_overflow=False)
                await self.websocket.send(data)
                await asyncio.sleep(0.005)
        except Exception as e:
            logging.error("音频传输出错: %s", e)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    async def message(self):
        """接收来自WebSocket服务端的消息"""
        try:
            while True:
                if self.websocket is None:
                    logging.error("WebSocket连接未建立")
                    return

                response = await self.websocket.recv()
                response_data = json.loads(response)
                text = response_data.get("text", "")
                self.offline_msg_done = response_data.get("is_final", False)

                if text:
                    self.result_text.append(text)

                if self.offline_msg_done:
                    print("识别完成")
                    break
        except Exception as e:
            logging.error("接收消息出错: %s", e)

    @asyncSlot()
    async def start_recognition(self):
        """开始识别"""
        self.offline_msg_done = False
        await self.connect_websocket()  # 连接WebSocket
        await asyncio.gather(self.record_microphone(), self.message())  # 开始录音和接收消息

    @asyncSlot()
    async def stop_recognition(self):
        """停止识别"""
        if self.websocket:
            await self.websocket.send(json.dumps({"action": "stop"}))
            await self.websocket.close()
            self.websocket = None
            self.result_text.append("识别已停止")

    def closeEvent(self, event):
        """关闭窗口时关闭WebSocket连接"""
        if self.websocket:
            asyncio.run(self.websocket.close())
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)

    # 使用QEventLoop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = SpeechRecognitionClient()
    window.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
