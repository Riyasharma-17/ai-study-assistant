import google.generativeai as genai
from dotenv import load_dotenv   #Loads variables from .env
import os       #Lets us access environment variables

load_dotenv()  #Reads:.env and loads its contents.

api_key = os.getenv("GEMINI_API_KEY")  #gets key from the environment

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key) #Configure the Gemini library using the API key stored in the variable api_key

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_answer(question, context):
    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer the question using only the provided context.
    """

    try:
        response = model.generate_content(prompt) #An object containing Gemini's generated output.
        return response.text

    except Exception as e:
        print(e)
        return "Failed to generate answer."