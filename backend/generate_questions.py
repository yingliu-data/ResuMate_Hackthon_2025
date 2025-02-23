import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import NamedTuple
import uuid

load_dotenv()
# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class InterviewBot():

    def __init__(self, job_profile=None, user_info=None):
        self.job_profile = job_profile
        self.user_info = user_info
        self.question_history = {}
    

    def clear_history(self):
        self.question_history = {}

    def generate_interview_questions(self, job_profile=None, user_info=None, message=None) -> tuple[int, str]:
        """
        Generates interview questions based on the job profile, skills, and initial message.

        Args:
            job_profile (str, optional): The job profile for the interview (e.g., "Software Engineer"). Defaults to None.
            user_info (str, optional): The skills of the candidate (e.g., "JavaScript, React, Node.js"). Defaults to None.
            message (str, optional): The initial message from the candidate. Defaults to None.

        Returns:
            str: A string containing the generated interview questions.
        """
        # Generate the system prompt
        if not job_profile:
            job_profile = self.job_profile
        
        if not user_info:
            user_infor = self.user_info

        interview_context = f"for a {job_profile} position" if job_profile else "for a technical role"
        system_prompt = f"You are a technical interviewer conducting an interview {interview_context}."
        
        if user_info:
            system_prompt += f" The candidate resume shared {user_info}."
        system_prompt += " Ask relevant technical questions and evaluate their responses. Please ask One question at a time and wait for candidate answer"

        # Prepare the messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message or "I'm ready to start the interview."}
        ]

        # Call OpenAI to generate the response
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,  # Adjust as needed
        )
        unique_question_id = uuid.uuid4()
        self.question_history[unique_question_id] = f"Question asked : {response.choices[0].message.content}"
        # Return the generated response
        return (unique_question_id, response.choices[0].message.content)

    
    def evaluate_answer(self, unique_question_id, user_answer):
        """
        Evaluates the accuracy of the user's answer to a given question.

        Args:
            unique_question_id (id): Unique identifier for original question asked.
            user_answer (str): The user's answer to the question.

        Returns:
            dict: A dictionary containing:
                - "is_correct" (bool): Whether the answer is correct.
                - "feedback" (str): Feedback on the user's answer.
        """
        # Generate the system prompt
        system_prompt = (
            "You are a technical interviewer evaluating a candidate's answer to a question. "
            "Determine if the answer is correct and provide feedback. "
            "If the answer is incorrect, explain why and provide the correct answer."
            "Please keep the response to 2 to 3 sentences. Assume feedback is to the candidate"
        )

        # Prepare the messages
        print(self.question_history)
        question = self.question_history[unique_question_id]
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {question}\nAnswer: {user_answer}"}
        ]

        # Call OpenAI to evaluate the answer
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=300,  # Adjust as needed
        )

        # Extract the evaluation from the response
        evaluation = response.choices[0].message.content

        # Determine if the answer is correct
        is_correct = "correct" in evaluation.lower()  # Simple heuristic; adjust as needed

        self.question_history[unique_question_id] = self.question_history[unique_question_id] + "  " + f"Is Answer Correct : {is_correct}"

        # Return the evaluation result
        return {
            "is_correct": is_correct,
            "feedback": evaluation
        }


# Example usage
if __name__ == "__main__":
    interview_me = InterviewBot(job_profile = "Software Engineer", user_info = "I am good at Python, AI")
    question_id, questions = interview_me.generate_interview_questions()
    print("Generated Interview Questions:")
    print(questions)
    answer = "I don't know the answer"
    print(answer)
    print(interview_me.evaluate_answer(question_id, answer))
    questions = interview_me.generate_interview_questions(message = f"Ask a harder question than last time. History is {interview_me.question_history}")
    