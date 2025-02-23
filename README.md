# ElevenLabs Hackathon 2025 - ResuMate  

## 🏆 About the Hackathon  
The **ElevenLabs Hackathon 2025** challenges participants to build innovative AI-driven applications using ElevenLabs and partner models/tools. Our team took on this challenge to create a product that helps job seekers optimize their resumes and ace interviews using AI-powered tools.  

## 🚀 About ResuMate  
ResuMate is an AI-powered interview and resume optimization assistant. It tailors resumes based on job descriptions, scrapes user profiles for insights, and conducts mock interviews to provide real-time feedback—helping job seekers put their best foot forward.  


## ⚙️ Installation (Run Locally)  

### 1. Clone the Repository  
```bash
git clone https://github.com/sophia172/ElevenLabs_Hackthon_2025
cd ElevenLabs_Hackthon_2025
```

### 2. Install Dependencies  
Open two terminals, one for Frontend and one for Backend.
#### Frontend  
```bash
cd frontend/link-sculptor
npm i
```

#### Backend  
Ensure you have **Python 3.10+** installed, then install the required packages:  
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables  
Copy `.env.example` to `.env` and fill in your API keys:  
```bash
cp .env.example .env
```
- `GROQ_API_KEY`: Your Groq API key.  
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key.  
- `OPENAI_API_KEY`: Your OpenAI API key.  
- `LANGSMITH_TRACING`: Boolean (`True` to enable tracing).  
- `LANGSMITH_API_KEY`: Your Langsmith API Key.  

### 4. Run the Servers  
Run the **frontend** and **backend** servers in separate terminal windows:  

#### Frontend  
```bash
cd frontend/link-sculptor
npm run dev
```
If this runs into an issue please run this below line and install again. Then try to run dev.
```bash
rm -rf node_modules package-lock.json
```

#### Backend  
```bash
cd backend
python user_profile.py
```

---

## 📑 Run the Extension  
1. Open **Google Chrome**.  
2. Navigate to the address returned in the **frontend server terminal**.  
3. Enter your details – you’re all set! 🚀  

---

## 🚀 About the Project  

- **What?**  
  ResuMate is your ultimate interview companion. It tailors your resume to match the job posting you provide and offers a personalized interview experience based on the job description and your background.  

- **Problem?**  
  ResuMate helps job seekers, professionals transitioning to new roles, and students navigating their career journey.  

- **Business Impact?**  
  With the potential to impact the global workforce, ResuMate helps users strengthen their fundamentals, practice interviews, and showcase their talent in the best light for job opportunities.  

---

## 🏆 Hackathon Details  

- **Hackathon Name:** ElevenLabs Hackathon 2025  
- **Challenge:** Build AI Agents using ElevenLabs & partner models/tools  

### Team Members  
- **Ying Liu** - [GitHub](https://github.com/sophia172)  
- **Joenam Coutinho** - [GitHub](https://github.com/joenamcoutinho)  
- **Tanuj Guha Thakurta** - [GitHub](https://github.com/hexcodeblaster)  
- **Sahana Venkatesh** - [GitHub](https://github.com/Sahanave)  

---

## 🎯 Key Features  

- **Enhanced Resume Optimization**: Automatically extracts key details from LinkedIn, GitHub, and the job role to refine and strengthen the resume.  
- **Tailored Resume**: Instantly generates a customized resume by analyzing user-provided information, including their existing resume, GitHub profile, job description, and LinkedIn profile.  
- **Personal Mock Interviewer**: Uses advanced LLM models and ElevenLabs to simulate interview questions, providing real-time feedback to improve response quality.  

---

## 🛠️ Tech Stack  

- **Frontend:** TypeScript (Lovable)  
- **Backend:** Python  
- **AI Models:** LLama, ElevenLabs, OpenAI  

---

## 🔗 Links  

- **Live Demo:** [Video]  
- **Presentation Deck:** [Slides]  

---

## 💡 Future Enhancements  

- **Personalized Cover Letter Generation**  
- **Coding Interview Feedback**  

---

## 📧 Contact  

**Name:** Sophia Liu  
📩 **Email:** sophia.j.liu@gmail.com  
