import os
from dotenv import load_dotenv
import google.generativeai as genai # Corrected import statement
from google.generativeai.types import GenerationConfig # Corrected config import

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

genai.configure(api_key=api_key)

def format_with_gemini(scraped_text: str, user_prompt: str) -> str:
    """
    Uses Google Gemini to process scraped webpage text according to the user-provided prompt.
    
    Args:
        scraped_text: The text content scraped from a webpage.
        user_prompt: The prompt provided by the user to guide the AI.

    Returns:
        A string containing the AI's processed output.

    Raises:
        RuntimeError: If the AI processing fails for any reason.
    """
    try:
        full_prompt = (
            f"User instructions: {user_prompt}\n\n"
            f"Website content:\n{scraped_text}"
        )

        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        response = model.generate_content(
            full_prompt,
            generation_config=GenerationConfig(temperature=0.7)
        )

        return response.text.strip()

    except Exception as e:
        raise RuntimeError(f"AI processing failed: {str(e)}")
