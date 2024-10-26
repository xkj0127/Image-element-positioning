import os
import pyttsx3
import websockets
import asyncio
import json
import logging
from multiprocessing import Process
from queue import Queue
import pyaudio
logging.basicConfig(level=logging.ERROR)
voices = Queue()
offline_msg_done = False

async def record_microphone():
    global voices
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=960)
    message = json.dumps({
        "mode": 'offline', "chunk_size": [5, 10, 5], "chunk_interval": 10,
        "wav_name": "microphone", "is_speaking": True, "hotwords": '', "itn": False
    })
    await websocket.send(message)
    while True:
        data = stream.read(960)
        await websocket.send(data)
        await asyncio.sleep(0.005)

async def record_from_scp():
    global offline_msg_done
    while not offline_msg_done:
        await asyncio.sleep(1)
    await websocket.close()

async def message():
    global websocket, offline_msg_done
    try:
        while True:
            response = await websocket.recv()
            response_data = json.loads(response)
            text = response_data.get("text", "")
            offline_msg_done = response_data.get("is_final", False)
            print("输入：", text)

    except Exception as e:
        print("Exception:", e)

async def ws_client():
    global websocket
    uri = "ws://localhost:10096"
    print("connect to", uri)
    async with websockets.connect(uri, subprotocols=["binary"], ping_interval=None) as websocket:
        await asyncio.gather(record_microphone(), message())

def run_ws_client():
    asyncio.run(ws_client())

if __name__ == '__main__':
    engine = pyttsx3.init()
    p = Process(target=run_ws_client)
    p.start()
    p.join()
    print('end')
