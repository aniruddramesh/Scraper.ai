import os
from dotenv import load_dotenv
import google.generativeai as genai # Corrected import statement
from google.generativeai.types import GenerationConfig # Corrected config import

# Load environment variables from the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Raise an error if the API key is not found
    raise ValueError("GEMINI_API_KEY is missing in .env file")

# Configure the genai library with the API key
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
        # Combine the user's prompt and the scraped content for the AI model
        full_prompt = (
            f"User instructions: {user_prompt}\n\n"
            f"Website content:\n{scraped_text}"
        )

        # Initialize the generative model. Using 'gemini-1.5-flash-latest' as it's the recommended model.
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Generate content with the model, including the generation_config
        response = model.generate_content(
            full_prompt,
            generation_config=GenerationConfig(temperature=0.7)
        )

        # Return the processed text
        return response.text.strip()

    except Exception as e:
        # Re-raise any exceptions as a RuntimeError for consistent error handling
        raise RuntimeError(f"AI processing failed: {str(e)}")
