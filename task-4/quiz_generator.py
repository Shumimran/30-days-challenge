import json
from typing import List, Dict, Any
from gemini_service import GeminiService

def generate_quiz(gemini_service: GeminiService, text: str, num_questions: int = 5) -> List[Dict[str, Any]]:
    """
    Generates multiple-choice quiz questions from the provided text using the Gemini API.
    The quiz questions are returned in a structured JSON format.

    Args:
        gemini_service (GeminiService): An instance of the GeminiService.
        text (str): The text content from which to generate quiz questions.
        num_questions (int): The desired number of quiz questions.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a quiz question.
                              Each dictionary will have keys like 'question', 'options', 'answer'.
                              Returns an empty list if no quiz can be generated or parsing fails.
    """
    if not text.strip():
        print("No text provided to generate quiz.")
        return []

    prompt = f"""
    Generate {num_questions} multiple-choice quiz questions from the following text.
    For each question, provide:
    - a 'question' string
    - an 'options' list of strings (at least 4 options)
    - an 'answer' string (the correct option)

    Format the output as a JSON array of objects.

    Example format:
    ```json
    [
      {{
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
      }}
    ]
    ```

    Text to generate questions from:
    {text}
    """
    
    quiz_json_str = gemini_service.generate_content(prompt)
    
    try:
        # The model might return the JSON string within markdown code block
        if quiz_json_str.strip().startswith("```json"):
            quiz_json_str = quiz_json_str.replace("```json", "").replace("```", "").strip()
        
        quiz_data = json.loads(quiz_json_str)
        if isinstance(quiz_data, list):
            return quiz_data
        else:
            print(f"Warning: Expected a JSON list, but got {type(quiz_data)}. Full response: {quiz_json_str}")
            return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from quiz generation: {e}")
        print(f"Raw response from Gemini API: {quiz_json_str}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during quiz generation: {e}")
        return []

