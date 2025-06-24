# ElevenLabs Hackathon 2025 - ResuMate  

## 🏆 About the Hackathon  
The **ElevenLabs Hackathon 2025** challenges participants to build innovative AI-driven applications using ElevenLabs and partner models/tools. Our team took on this challenge to create a product that helps job seekers optimize their resumes and ace interviews using AI-powered tools.  

## 🚀 About ResuMate  
ResuMate is an AI-powered interview and resume optimisation assistant. 
It tailors resumes based on 
- job descriptions. 
- Look into user profiles for insights.
- Conducts mock interviews to provide real-time feedback—helping job seekers.  


## ⚙️ Installation (Run Locally)  

### 1. Clone the Repository  
```bash
git clone https://github.com/yingliu-data/ElevenLabs_Hackthon_2025
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
- 

### 4. Run the Servers  
Run the **frontend** and **backend** servers in separate terminal windows:  

#### Frontend  
```bash
cd frontend/link-sculptor
npm run dev
```

#### Backend  
```bash
cd backend
python user_profile.py
```
#### Trouble Shooting  

1. If you runs into an issue during start up of front end server, please run this below line and install again. Then try to run dev.
```bash
rm -rf node_modules package-lock.json
```
```bash
cd frontend/link-sculptor
npm i
npm run dev
```
2. If there an issue with rendering frontend and issue like one attached, 
```bash
[plugin:vite:import-analysis] Failed to resolve import "@/lib/utils" from "src/components/ui/card.tsx". Does the file exist?
```
1. Clone link-sculptor by running 
```bash
https://github.com/hexcodeblaster/link-sculptor
```
2. Copy everything to link-sculptor file except git files.
3.
```bash
rm -rf node_modules package-lock.json
```
4. Run npm install and npm run dev again 
```bash
cd frontend/link-sculptor
npm i
npm run dev
```
#### Backend  
```bash
cd backend
python user_profile.py
```

---


#### Troubleshooting
1. If there an issue with installation, please do this 
```bash
rm -rf node_modules package-lock.json
```
Then run 



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
- **Ying Liu** - [GitHub](https://github.com/yingliu-data)  
- **Joenam Coutinho** - [GitHub](https://github.com/joenamcoutinho)  
- **Tanuj Guha Thakurta** - [GitHub](https://github.com/hexcodeblaster)  
- **Sahana Venkatesh** - [GitHub](https://github.com/Sahanave)  

---

## 🎯 Key Features  
- **Tailored Resume**: Instantly generates a customised resume by analyzing user-provided information, including their existing resume, GitHub profile, job description, and LinkedIn profile.
- **Enhanced Resume Optimization**: Automatically extracts key details from LinkedIn, GitHub, and the job role to refine and strengthen the resume.  
- **Tailored Cover Letter**: Instantly generates a customised cover letter by analysing user-provided information and the job description.
- **Personal Mock Interviewer**: Uses advanced LLM models and ElevenLabs to simulate the interview process, asking job-specific questions and providing real-time feedback to improve response quality.
---

## 🛠️ Tech Stack  

- **Frontend:** TypeScript (Lovable)  
- **Backend:** Python  
- **AI Models:** LLama, ElevenLabs, OpenAI, Langchain
---

## 🔗 Links  

- **Live Demo:** [Video]  

---

## 💡 Future Enhancements  

- **Add GitHub Code quality and competence analysis**  
- **Coding Interview Feedback**  

---

## 📧 Contact  

**Name:** Ying Liu  
📩 **Email:** ying.liu@yingliu.site
