import json


def safe_json_parse(raw_output):
    """
    Safely convert the model's response into a Python dictionary.

    If the model accidentally returns Markdown JSON fences
    or extra text, try to clean it before parsing.
    """

    if not raw_output:
        return None

    cleaned_output = raw_output.strip()

    # Remove ```json and ``` fences if the model adds them
    if cleaned_output.startswith("```json"):
        cleaned_output = cleaned_output[7:]

    elif cleaned_output.startswith("```"):
        cleaned_output = cleaned_output[3:]

    if cleaned_output.endswith("```"):
        cleaned_output = cleaned_output[:-3]

    cleaned_output = cleaned_output.strip()

    try:
        return json.loads(cleaned_output)

    except json.JSONDecodeError: 
        return None


def validate_assessment(data):
    """
    Check whether the parsed response contains
    all required fields.
    """

    required_fields = [
        "summary",
        "possible_conditions",
        "urgency_level",
        "recommended_next_steps",
        "questions_for_doctor",
        "warning_signs"
    ]

    if not isinstance(data, dict):
        return False

    return all(field in data for field in required_fields)