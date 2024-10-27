import time
from functools import wraps
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
model_dir = "iic/SenseVoiceSmall"
model = AutoModel(
    model=model_dir,
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cuda:0",
)
def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 调用被装饰的函数
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算执行时间
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper

@timer_decorator
def main2():
    # en
    res = model.generate(
        input=r"./inputs/recording.wav",
        cache={},
        language="zn",  # "zn", "en", "yue", "ja", "ko", "nospeech"
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15,
    )
    text = rich_transcription_postprocess(res[0]["text"])
    print(text)



main2()