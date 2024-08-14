
import websockets
import asyncio
import json
from multiprocessing import Process
from queue import Queue
import pyaudio



words_max_print = 10000
globals_chunk_size = [5, 10, 5]
voices = Queue()
offline_msg_done = False


# 麦克风输入
async def record_microphone():
    global voices
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    chunk_size = 60.0
    CHUNK = int(RATE / 1000 * chunk_size)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,              # 采样深度
                    channels=CHANNELS,          # 获取声道数
                    rate=RATE,                  # 获取采样率
                    input=True,                 # 输入
                    frames_per_buffer=CHUNK)    # 采样点缓存数量



    message = json.dumps({"mode": "offline", "chunk_size": globals_chunk_size, "chunk_interval": 10,
                          "wav_name": "microphone", "is_speaking": True, "hotwords": json.dumps({}), "itn": True})
    # voices.put(message)
    await websocket.send(message)
    while True:
        data = stream.read(CHUNK)
        message = data
        # voices.put(message)
        await websocket.send(message)
        await asyncio.sleep(0.005)



async def message(id):
    global websocket, voices, offline_msg_done
    text_print_2pass_offline = ""

    try:
        while True:

            meg = await websocket.recv()
            meg = json.loads(meg)
            print(meg)
            text = meg["text"]
            offline_msg_done = meg.get("is_final", False)
            if 'mode' not in meg:
                continue
            text_print_2pass_offline += "{}".format(text)
            print("输入：" + text)
            print("输出：" + text)
            message22 = [
                {'role': 'user', 'content': text}
            ]
            from qwen_agent.llm import get_chat_model
            result = get_chat_model({
                'model': 'qwen2',
                'model_server': 'http://127.0.0.1:11434/v1',
                'generate_cfg': {
                    'top_p': 0.8
                }
            }).chat(
                messages=message22,
                stream=False)
            print(result)
    except Exception as e:
        print("Exception:", e)


async def ws_client(id, chunk_begin, chunk_size):
    global websocket, voices, offline_msg_done
    for i in range(chunk_begin, chunk_begin + chunk_size):
        offline_msg_done = False
        voices = Queue()
        uri = "ws://127.0.0.1:10096"
        ssl_context = None
        print("connect to", uri)
        async with websockets.connect(uri, subprotocols=["binary"], ping_interval=None, ssl=ssl_context) as websocket:
            task = asyncio.ensure_future(record_microphone())
            task2 = asyncio.ensure_future(message(str(id) + "_" + str(i)))
            await asyncio.gather(task, task2)
    exit(0)


def one_thread(id, chunk_begin, chunk_size):
    asyncio.get_event_loop().run_until_complete(ws_client(id, chunk_begin, chunk_size))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    p = Process(target=one_thread, args=(1, 0, 1))
    p.start()
    p.join()
    print('end')

