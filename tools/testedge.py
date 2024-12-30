import os
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
import uvicorn
from PIL import Image
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from paddleocr import PaddleOCR
import warnings

warnings.filterwarnings("ignore")

os.makedirs("uploads", exist_ok=True)

# Initialize models
model_dir = "iic/SenseVoiceSmall"
model = AutoModel(
    model=model_dir,
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cuda:0",
)
ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)


def get_ocr(path, key):
    text = ocr.ocr(path)
    for i in text[0]:
        if key in i[1][0]:
            position = i[0]
            (top_left, _, bottom_right, _) = position
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            target_x = (top_left[0] + bottom_right[0]) // 2
            target_y = (top_left[1] + bottom_right[1]) // 2
            return target_x, target_y
    return None


app = FastAPI()

@app.post("/upload")
async def upload(audio: UploadFile = File(...), image: UploadFile = File(...)):
    audio_path = f"uploads/{audio.filename}"
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    try:
        res = model.generate(
            input=audio_path,
            cache={},
            language="zn",
            use_itn=True,
            batch_size_s=60,
            merge_vad=True,
            merge_length_s=15,
        )
        audio_text = rich_transcription_postprocess(res[0]["text"])
    except Exception:
        return {"status": "error", "message": "Audio transcription failed."}

    # Save the image
    image_data = await image.read()
    img = Image.open(BytesIO(image_data))
    screenshot_path = "uploads/screenshot.png"
    img.save(screenshot_path)

    # Get OCR coordinates
    result = get_ocr(screenshot_path, audio_text)
    if not result:
        return {"status": "error", "message": "OCR did not find coordinates."}

    x, y = result
    return {"coordinates": {"x": x, "y": y}, "status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
