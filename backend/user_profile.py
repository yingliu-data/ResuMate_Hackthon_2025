from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI(title="User Profile API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create storage directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to the User Profile API"}


@app.post("/user-profile/")
async def user_profile(
        github_link: str = Form(...),
        linkedin_link: str = Form(...),
        resume: Optional[UploadFile] = File(None),
        job_description: Optional[UploadFile] = File(None)
):
    try:
        # Create user_profile record
        user_profile = {
            "timestamp": datetime.now().isoformat(),
            "github_link": github_link,
            "linkedin_link": linkedin_link,
            "resume_path": None,
            "job_description_path": None
        }
        # Handle job description upload (required)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        jd_filename = f"{timestamp}_jd_{job_description.filename}"
        jd_filepath = os.path.join(UPLOAD_DIR, jd_filename)

        with open(jd_filepath, "wb") as buffer:
            content = await job_description.read()
            buffer.write(content)

        user_profile["job_description_path"] = jd_filepath

        # Handle resume upload if provided
        if resume:
            resume_filename = f"{timestamp}_resume_{resume.filename}"
            resume_filepath = os.path.join(UPLOAD_DIR, resume_filename)

            with open(resume_filepath, "wb") as buffer:
                content = await resume.read()
                buffer.write(content)

            user_profile["resume_path"] = resume_filepath

        return {
            "message": "Application submitted successfully",
            "job_description_path": user_profile["job_description_path"],
            "resume_path": user_profile["resume_path"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/conversation/')
async def conversation():
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)