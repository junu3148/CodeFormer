
import os
from fastapi import FastAPI, Response, Form
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess 
import json 
import shutil
from typing import Optional
from datetime import datetime

# uvicorn main:app --reload --host 192.168.0.48 
# 서버 실행 

def get_current_time_text():
    """Return the current time as a formatted text string."""
    now = datetime.now()
    time_text = now.strftime("_%Y%m%d_%H%M%S")
    return time_text

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

import os

@app.post("/video")
async def upload_video(video: UploadFile = File(...), scaleOption: Optional[str] = Form(None)):
    video_name_all = video.filename
    video_file = video.file
    video_name = video_name_all.split('.')[0]
    extension = video_name_all.split('.')[-1]
    time_name = get_current_time_text() 
    video_name_all = f"{video_name}{time_name}.{extension}"
    input_path = f"./input_video/{video_name}/"

    output_path = f"./output_video/{video_name}/"
    os.makedirs(input_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    

    if scaleOption:
        scale_option = json.loads(scaleOption)
        scale_option = str(scaleOption)
    else:
        scale_option = None
    
    input_full_path = os.path.join(input_path, video_name_all)
    output_full_path = os.path.join(output_path, video_name_all)

    # try:
    with open(input_full_path, "wb") as buffer:
        while content := await video.read(1024):
            buffer.write(content)
        
    subprocess.call(['python', 'c:/lumen/upscale/CodeFormer/inference_codeformer.py',
                        '-i', input_full_path,
                        '-o', output_path,
                        '-s', scale_option,
                        '--face_upsample'
                        ])
        
    return FileResponse(output_full_path, media_type='video/mp4', filename=video_name_all)
    # finally:
    #     if os.path.exists(input_path):
    #         shutil.rmtree(input_path)
    #     if os.path.exists(output_path):
    #         shutil.rmtree(output_path)


