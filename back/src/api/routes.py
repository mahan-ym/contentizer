import os
import shutil
import ffmpeg
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from src.services.uuid import gen_uuid_str

router = APIRouter()

# Define assets directory relative to project root (back/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(ASSETS_DIR, exist_ok=True)

class TrimRequest(BaseModel):
    filename: str
    start_time: float
    end_time: float

class PromptRequest(BaseModel):
    prompt: str
    filename: str

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        project_unique_id = gen_uuid_str()
        os.mkdir(os.path.join(ASSETS_DIR, project_unique_id))
        new_project_directory = os.path.join(ASSETS_DIR, project_unique_id)
        new_filename = f"{gen_uuid_str()}{file.filename}"

        file_path = os.path.join(new_project_directory, new_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": new_filename, "url": f"/api/stream/{new_filename}"}
    except Exception as e:
        print(e.__str__())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream/{filename}")
async def stream_video(filename: str, range: Optional[str] = None):
    file_path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_size = os.path.getsize(file_path)
    
    # Simple full file response for now, or use range handling similar to previous nextjs app
    # FastAPI's FileResponse handles ranges automatically if headers are passed? 
    # Actually FileResponse doesn't strictly support Range header out of box for video seeking in all cases without extra setup.
    # But for simplicity let's try FileResponse first. If seeking breaks we can implement manual streaming generator.
    
    # Implementing manual range handling for better video support
    start = 0
    end = file_size - 1
    
    if range:
        range_str = range.replace("bytes=", "")
        range_parts = range_str.split("-")
        if range_parts[0]:
            start = int(range_parts[0])
        if len(range_parts) > 1 and range_parts[1]:
            end = int(range_parts[1])
            
    chunk_size = end - start + 1
    
    def iterfile():
        with open(file_path, "rb") as video:
            video.seek(start)
            yield video.read(chunk_size)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Type": "video/mp4",
    }
    
    return StreamingResponse(iterfile(), status_code=206, headers=headers)

@router.post("/trim")
async def trim_video(request: TrimRequest):
    input_path = os.path.join(ASSETS_DIR, request.filename)
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    output_filename = f"trimmed_{request.filename}"
    output_path = os.path.join(ASSETS_DIR, output_filename)
    
    try:
        (
            ffmpeg
            .input(input_path, ss=request.start_time, to=request.end_time)
            .output(output_path, c="copy") # Stream copy is faster, but might need re-encoding if keyframes don't align
            .overwrite_output()
            .run(quiet=True)
        )
        return {"filename": output_filename, "url": f"/api/stream/{output_filename}"}
    except ffmpeg.Error as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")

@router.post("/agent/prompt")
async def get_agent_prompt(request: PromptRequest):
    print(f"Received prompt for {request.filename}: {request.prompt}")
    
