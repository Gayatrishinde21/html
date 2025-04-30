import os
from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from datetime import datetime
import uvicorn
from db import SessionLocal, engine
from model import Biodata, Base

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

# Templates and upload folder
templates = Jinja2Templates(directory="templates")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

# Show form
@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Handle submission
@app.post("/submit")
async def submit_form(
    fname: str = Form(...),
    lname: str = Form(...),
    address: str = Form(...),
    date: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    gender: str = Form(...),
    hobbies: List[str] = Form(...),
    photo: UploadFile = File(...)
):
    # Save photo
    photo_path = os.path.join(UPLOAD_FOLDER, photo.filename)
    with open(photo_path, "wb") as f:
        f.write(await photo.read())

    # Parse date and hobbies
    dob = datetime.strptime(date, "%Y-%m-%d").date()
    hobbies_str = ", ".join(hobbies)

    # Insert into DB
    db = SessionLocal()
    new_entry = Biodata(
        fname=fname,
        lname=lname,
        address=address,
        dob=dob,
        phone=phone,
        email=email,
        gender=gender,
        photo=photo_path,
        hobbies=hobbies_str
    )
    db.add(new_entry)
    db.commit()
    db.close()

    return {"message": "Biodata submitted successfully!"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000
    )
    
