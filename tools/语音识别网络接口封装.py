from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import os


app = FastAPI()
UPLOAD_FOLDER = 'wav_files'  # 确保该目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 初始化模型
## 语音识别模型
model_dir = "iic/SenseVoiceSmall"
model = AutoModel(
    model=model_dir,
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cuda:0",
)



# 主识别函数
async def recognize_audio(file_path: str):
    res = model.generate(
        input=file_path,
        cache={},
        language="zn",  # "zn", "en", "yue", "ja", "ko", "nospeech"
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15,
    )
    text = rich_transcription_postprocess(res[0]["text"])
    return text


@app.post("/recognize_audio")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as file_object:
        file_object.write(await file.read())
    try:
        result_text = await recognize_audio(file_location)
        return result_text
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 启动FastAPI服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.43.7", port=8000)
