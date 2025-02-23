
import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
import getpass
from typing_extensions import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from generate_questions import InterviewBot
from backend.text_speech_convert import text2speech, speech2text
from data_scraper import linkedin_data, github_data, resume_data, jd_data
import validators

if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")



llm = init_chat_model("mixtral-8x7b-32768", model_provider="groq")

# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["CV", "Cover Letter", "Interview"] = Field(
        None, description="The next step in the routing process"
    )


# Augment the LLM with schema for structured output
router = llm.with_structured_output(Route)


# State
class State(TypedDict):
    input: str
    decision: str
    output: str
    person_context: str
    job_context: str
    user_id: int
    flag: str

class HrAgent():
    def __init__(self, user_profile=None):
        linkedindata = linkedin_data(user_profile["linkedin_link"])

        githubdata = github_data(user_profile["github_link"])

        jobdata = jd_data(user_profile["job_description"])

        cvdata = resume_data(user_profile["resume_path"])
        person_context = self.clean_person_context(f"""Linkedin info: {linkedindata} 
                                                        GitHub Info: {githubdata}
                                                        User's CV draft: {cvdata}""")

        job_context = self.clean_job_context(jobdata)
        self.interviewBot = InterviewBot(job_profile=job_context,
                                    user_info=person_context)
        self.job_context = job_context
        self.person_context = person_context

        # Build workflow
        self.router_builder = StateGraph(State)

        # Add nodes
        self.router_builder.add_node("generate_CoverLetter", self.generate_cover_letter)
        self.router_builder.add_node("Strike_Interview", self.strike_interview)
        self.router_builder.add_node("generate_CV", self.generate_CV)
        self.router_builder.add_node("llm_call_router", self.llm_call_router)

        # Add edges to connect nodes
        self.router_builder.add_edge(START, "llm_call_router")

        self.router_builder.add_conditional_edges(
            "llm_call_router",
            self.route_decision,
            {  # Name returned by route_decision : Name of next node to visit
                "generate_CoverLetter": "generate_CoverLetter",
                "Strike_Interview": "Strike_Interview",
                "generate_CV": "generate_CV",
            },
        )
        self.router_builder.add_edge("generate_CoverLetter", END)
        self.router_builder.add_edge("generate_CV", END)

        # Compile workflow
        self.router_workflow = self.router_builder.compile()

    def __call__(self, new_messgae):
        if new_messgae and os.path.exists(new_messgae):
            new_messgae = speech2text(new_messgae)
        state = self.router_workflow.invoke({
            "input": new_messgae,
            "job_context": self.job_context,
            "person_context": self.person_context
        })
        output = {"message": None,
                  "content": None}
        if new_messgae and os.path.exists(new_messgae):
            if state["flag"] != "Interview":
                output["message"] = text2speech("Here is your " + state["flag"])
                output["content"] = state["output"]
            else:
                output["message"] = text2speech("Here is your " + state["flag"])
                output["content"] = None
        else:
            if state["flag"] != "Interview":
                output["message"] = "Here is your " + state["flag"]
                output["content"] = state["output"]
            else:
                output["message"] = state["output"]
                output["content"] = None

        return output

        # Nodes
    def generate_cover_letter(self, state: State):
        """Write a Cover Letter"""

        prompt = f"""
                    Here is the personal information:
                    {state["person_context"]}.
    
                    Here is the Job information:
                    {state["job_context"]}
    
                    Based on the following information, create a professional and detailed Cover Letter:
    
                    Ensure the CV includes sections for:
                    1. Header
                    Your name, email, phone number, and optionally your LinkedIn profile.
                    Date of submission.
                    Hiring manager’s name, company, and address (if available).
                    2. Salutation
                    Address the hiring manager by name (e.g., Dear [Hiring Manager’s Name]).
                    If the name isn’t available, use Dear Hiring Manager instead.
                    3. Introduction
                    Clearly state the position you're applying for.
                    A compelling hook—why you're interested in the role or company.
                    A sentence summarizing why you're a strong candidate.
                    4. Body (1-2 paragraphs)
                    Highlight relevant experience: Connect your skills and past achievements to the job requirements.
                    Show enthusiasm for the company: Mention something specific about the company’s work or mission that excites you.
                    Provide evidence: Use a brief example to demonstrate your skills in action.
                    5. Closing Paragraph
                    Express enthusiasm about the opportunity to discuss your qualifications further.
                    Politely request an interview.
                    Thank the reader for their time.
                    6. Signature
                    Sign off with Sincerely or Best regards, followed by your name.
    
                    Format it in a clear and concise markdown structure. No greetings, introductions, or unnecessary text.
                    """
        result = llm.invoke(prompt)
        return {"output": result.content, "flag": "Cover Letter"}

    def strike_interview(self, state: State):
        """Write an Interview question"""
        _, bot_word = self.interviewBot.generate_interview_questions()
        return {"output": bot_word, "flag": "Interview"}

    def clean_person_context(self, person_context):
        prompt = f"""
            This is messy personal information from the user:
            {person_context}
            Clean this data to a paragraph within 200 words.
            No greetings, introductions, or unnecessary text.
        """
        result = llm.invoke(prompt)
        return result.content

    def clean_job_context(self, job_context):
        prompt = f"""
                    This is messy job description information from a website:
                    {job_context}
                    If the content is None, return None as well. If the content is not None:
                    There is only one job listed on the website, find the job and it's description first. 
                    Clean the description to a paragraph within 200 words.
                    No greetings, introductions, or unnecessary text.
                """
        result = llm.invoke(prompt)
        return result.content

    def generate_CV(self, state: State):
        """Write a CV"""
        prompt = f"""
                Here is the personal information:
                {state["person_context"]}.
    
                Here is the Job information:
                {state["job_context"]}
    
                Based on the following information, create a professional and detailed CV:
    
                Ensure the CV includes sections for:
                - Personal Information
                - Professional Summary
                - Work Experience
                - Education
                - Skills
                - Certifications (if applicable)
    
                Format it in a clear and concise markdown structure. No greetings, introductions, or unnecessary text.
                """
        result = llm.invoke(prompt)
        return {"output": result.content, "flag": "CV"}

    def llm_call_router(self, state: State):
        """Route the input to the appropriate node"""

        # Run the augmented LLM with structured output to serve as routing logic
        decision = router.invoke(
            [
                SystemMessage(
                    content="Route the input to Cover Letter, Interview, or CV based on the user's request."
                ),
                HumanMessage(content=state["input"]),
            ]
        )
        return {"decision": decision.step}

    # Conditional edge function to route to the appropriate node
    def route_decision(self, state: State):
        # Return the node name you want to visit next
        if state["decision"] == "Cover Letter":
            return "generate_CoverLetter"
        elif state["decision"] == "Interview":
            return "Strike_Interview"
        elif state["decision"] == "CV":
            return "generate_CV"





if __name__ == "__main__":
    user_profile = {}
    user_profile["linkedin_link"] = "https://www.linkedin.com/in/yingliu-data/"
    user_profile["github_link"] = "sophia172"
    user_profile["job_description"] = "software engineer"
    user_profile["resume_path"] = "xyz"
    agent = HrAgent(user_profile=user_profile)
    output = agent("give me a interview")
    print(output)
