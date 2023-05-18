import shutil
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File

from lib import config

router = APIRouter()


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise Exception("File is not provided")
        images_directory = Path(config.UPLOAD_IMAGE_PATH)
        images_directory.mkdir(parents=True, exist_ok=True)
        file_path = images_directory / file.filename

        with open(file_path, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return the file path
        saved_path = file_path.parts.index("static")
        file_path = str(file_path)
        file_path = file_path[saved_path+6:].replace("\\", "/")
        return {"file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))