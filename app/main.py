from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import schemas
import crud
import models
from database import get_db, engine, SessionLocal
from typing import List, Dict
import uuid
from utils import perform_translation
import time
from pydantic import BaseModel
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Setup for Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows only localhost:8000
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers 
)

# @app.post("/translate", response_model=schemas.TaskResponse)
# def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

#     # Create a new translation task
#     task = crud.create_translation_task(db, request.text, request.languages)

#     background_tasks.add_task(perform_translation, task.id, request.text, request.languages, db)

#     return {"task_id": task.id}


# @app.get("/translate/{task_id}", response_model=schemas.TranslationStatus)
# def get_translate(task_id: int , db: Session = Depends(get_db)):

#     # Create a new translation task
#     task = crud.get_translation_task(db, task_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="task not found")
#     return {"task_id": task.id, "status": task.status, "translation":task.translations}



# @app.get("/translate/content/{task_id}")
# def get_translate_content(task_id: int , db: Session = Depends(get_db)):

#     # Create a new translation task
#     task = crud.get_translation_task(db, task_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="task not found")
#     return task

@app.post("/translate", response_model=schemas.TaskResponse)
def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    # Create a new translation task
    task = crud.create_translation_task(db, request.text, request.languages)

    background_tasks.add_task(perform_translation, task.id, request.text, request.languages, db)

    return {"task_id": task.id}

@app.get("/translate/{task_id}", response_model=schemas.TranslationStatus)
def get_translate(task_id: int, db: Session = Depends(get_db)):

    # Retrieve the translation task
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    
    return {"task_id": task.id, "status": task.status, "translations": task.translations}

@app.get("/translate/content/{task_id}")
def get_translate_content(task_id: int, db: Session = Depends(get_db)):

    # Retrieve the translation task content
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")

    # return {"task_id": task_id, "translations": task.translations or {}}
    return task

# Dummy storage for tasks
# class TranslationRequest(BaseModel):
#     text: str
#     languages: List[str]

# class TranslationResponse(BaseModel):
#     task_id: int
#     status: str
#     translations: Dict[str, str]

# # Dummy storage for tasks
# tasks = {}

# @app.post("/translate", response_model=TranslationResponse)
# async def translate(request: TranslationRequest, background_tasks: BackgroundTasks):
#     task_id = len(tasks) + 1
#     tasks[task_id] = {"status": "in progress", "translations": {}}

#     # Run translation in the background
#     background_tasks.add_task(run_translation, task_id, request.text, request.languages)

#     return {"task_id": task_id, "status": "in progress", "translations": {}}

# @app.get("/translate/{task_id}", response_model=TranslationResponse)
# async def get_translation(task_id: int):
#     if task_id not in tasks:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return {"task_id": task_id, "status": tasks[task_id]["status"], "translations": tasks[task_id]["translations"]}

# async def run_translation(task_id: int, text: str, languages: List[str]):
#     import time
#     # Simulate translation work
#     time.sleep(5)
    
#     translations = {lang: f"{text} translated to {lang}" for lang in languages}
    
#     tasks[task_id] = {"status": "completed", "translations": translations}

# @app.get("/translate/content/{task_id}")
# async def get_translation_content(task_id: int):
#     if task_id not in tasks:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return tasks[task_id]["translations"]
