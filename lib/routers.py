import os
import shutil

from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File

router = APIRouter()


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise Exception("File is not provided")
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        images_directory = os.path.join(current_file_directory, "../static/images")
        os.makedirs(images_directory, exist_ok=True)
        file_path = os.path.join(images_directory, file.filename)

        with open(file_path, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return the file path
        return {"file_path": file_path, "info": f"file '{file.filename}' saved at '{file_path}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        file.file.close()
