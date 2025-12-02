import google.generativeai as genai
import os

class GeminiService:
    """
    A service class to interact with the Google Gemini API.
    """
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """
        Initializes the GeminiService with an API key and model name.

        Args:
            api_key (str): Your Google Gemini API key.
            model_name (str): The name of the Gemini model to use (e.g., "gemini-pro").
        """
        if not api_key:
            raise ValueError("Gemini API key cannot be empty.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        print(f"GeminiService initialized with model: {model_name}")

    def generate_content(self, prompt: str) -> str:
        """
        Generates content using the configured Gemini model based on the given prompt.

        Args:
            prompt (str): The text prompt to send to the Gemini model.

        Returns:
            str: The generated text content from the Gemini model.
        """
        try:
            response = self.model.generate_content(prompt)
            # Access the text directly from the Candidate object within the response
            # Assuming the first candidate is the desired one and has text
            if response.candidates:
                # Ensure parts exist before accessing
                if response.candidates[0].content.parts:
                    return response.candidates[0].content.parts[0].text
                else:
                    print("Warning: Candidate has no content parts.")
                    return "No content generated."
            else:
                return "No content generated."
        except Exception as e:
            print(f"Error generating content with Gemini API: {e}")
            return f"Error: {e}"

