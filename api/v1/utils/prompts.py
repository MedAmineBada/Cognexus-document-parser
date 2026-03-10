"""
This module contains prompts used for organizing and structuring extracted text.
"""
# This prompt is used to guide an AI model in cleaning and structuring raw text extracted from an exam PDF into a JSON format.
organize_text_prompt = """
    You will receive raw text extracted from an exam PDF. The text may contain noise such as headers, page numbers, formatting artifacts, and repeated titles.

    Your task is to clean the content and convert it into structured JSON.

    Remove:
    - headers
    - footers
    - page numbers
    - repeated exam titles
    - formatting artifacts

    Keep:
    - images as placeholders if present (e.g., [IMAGE_1])
    - the logical structure of exercises

    OUTPUT FORMAT

    Return ONLY valid JSON.

    Structure:

    {
      "1": {
        "text": "main description or problem statement",
        "grading": "total points of the exercise",
        "given": ["list of given values, assumptions, constants"],
        "examples": ["examples provided in the exercise"],
        "questions": {
          "1": {
            "question": "question text",
            "grade": "points if specified, otherwise null"
          }
        }
      }
    }

    RULES
    1. Each exercise must be keyed by its number.
    2. Do not invent information.
    3. Return ONLY JSON. Do NOT wrap the result in ```json``` or markdown.

    Now process the following raw extracted exam text:

    """