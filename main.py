import json

from LLM_tools import LLMClient
from get_position import get_position

if __name__ == '__main__':
    client = LLMClient()
    # 第三步，发起交互
    message = [
        {'role': 'user', 'content': "我要看学霸，把声音设置为20，再帮我点击最帅召唤物"}
    ]
    ops = client.ask(message)[0].get('function_call').get('arguments')
    ops = json.loads(ops)
    print(ops.get('watch',[None]))
    element = ops.get('watch',[None])
    if element:
        print(element[0].strip("播放"))
        get_position(element[0].strip("播放"))

