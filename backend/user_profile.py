from aiohttp.web_fileresponse import content_type
from fastapi import FastAPI, HTTPException, Form, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from multipart import file_path
from openai import files
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn
from datetime import datetime
import os
import tempfile
from agent_distribution import HrAgent

# Initialize FastAPI app
app = FastAPI(title="User Resume Helper")

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

hr_agent = None

class ChatRequest(BaseModel):
    message: str

@app.post("/chat/")
async def chat_endpoint(request: ChatRequest) -> Dict[str, str]:
    try:
        user_message = request.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        global hr_agent
        if hr_agent:
            return_response = hr_agent(user_message).get("message")
        else:
            return_response = "Please initialise your profile first by providing github username,LinkedIn profile link, and the job description url"

        return {"message": return_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.post("/chat/audio/")
async def process_audio(audio: UploadFile = File(...)):
    """
    Receives an uploaded audio file, transcribes it, and returns the text.
    """
    try:
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(audio.filename)[-1] or ".webm"
        filename = f"{timestamp}_recording{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        generate_cv = False
        is_file_link = None
        global hr_agent
        if hr_agent:
            agent_response = hr_agent(file_path)
            if agent_response.get("content",False):
                generate_cv = True
            is_file_link = os.path.exists(agent_response.get("message",None) )
        else:
            agent_response = "Please initialise your profile first by providing github username,LinkedIn profile link, and the job description url"
        audio_data = None
        if is_file_link:
            with open(os.path.join(agent_response.get("message"))) as audio_file:
                audio_data = audio_file.read()

        return_response = {"message":audio_data,
                           "generateCV": generate_cv}
        return return_response

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Welcome to the User Profile API"}


@app.post("/user-profile/")
async def user_profile(
        github_link: str = Form(...),
        linkedin_link: str = Form(...),
        resume: Optional[UploadFile] = File(None),
        job_description: str = Form(...)

):
    try:
        # Create user profile record
        user_profile = {
            "github_link": github_link,
            "linkedin_link": linkedin_link,
            "job_description": job_description,
            "resume_path": None
        }

        # Handle resume upload if provided
        if resume:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            resume_filename = f"{timestamp}_resume_{resume.filename}"
            resume_filepath = os.path.join(UPLOAD_DIR, resume_filename)

            with open(resume_filepath, "wb") as buffer:
                content = await resume.read()
                buffer.write(content)

            user_profile["resume_path"] = resume_filepath

        global hr_agent
        hr_agent = HrAgent(user_profile=user_profile)#
        response = hr_agent("Generate CV")
        message = {}
        message['cv'] =response.get("content")
        print(response)
        return message

    except Exception as e:
        print("exception: ",e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)