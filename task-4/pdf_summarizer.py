from gemini_service import GeminiService

def summarize_pdf_text(gemini_service: GeminiService, pdf_text: str) -> str:
    """
    Generates a summary of the provided PDF text using the Gemini API.

    Args:
        gemini_service (GeminiService): An instance of the GeminiService.
        pdf_text (str): The extracted text content from a PDF document.

    Returns:
        str: A concise summary of the PDF text.
    """
    if not pdf_text.strip():
        return "No text provided to summarize."

    prompt = f"Please summarize the following document text concisely:\n\n{pdf_text}"
    summary = gemini_service.generate_content(prompt)
    return summary


