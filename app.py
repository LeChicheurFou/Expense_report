from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
import uuid

from backend import ImageAgent
from sqlitedb import save_ndf

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

agent = ImageAgent()


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/extract")
async def extract(file: UploadFile = File(...)):

    filename = f"uploads/{uuid.uuid4()}_{file.filename}"

    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = agent.ask_vision_model(filename)

    return {
        "image_path": filename,
        "data": data
    }


@app.post("/save")
async def save(payload: dict):

    save_ndf(
        payload["image_path"],
        payload["data"]
    )

    return {"success": True}