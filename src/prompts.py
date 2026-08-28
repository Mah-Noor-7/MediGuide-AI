from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage


# ---------------------------------------------------------
# Medical safety instructions
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are MediGuide AI, an educational medical information assistant.

IMPORTANT SAFETY RULES:
- You are NOT a doctor.
- Do NOT provide a confirmed medical diagnosis.
- Do NOT claim certainty about any medical condition.
- Possible conditions are for educational information only.
- Encourage the user to consult a qualified healthcare professional.
- If symptoms may indicate an emergency, clearly advise the user
  to seek emergency medical help immediately.
- Be calm, clear, respectful, and easy to understand.
- Never recommend stopping or changing prescribed medication.
- Always mention that this is educational guidance, not professional
  medical advice.

Return ONLY valid JSON.
Do not use Markdown.
Do not add any text before or after the JSON.
"""


# ---------------------------------------------------------
# Required JSON structure
# ---------------------------------------------------------

JSON_SCHEMA_INSTRUCTION = """
Return the response using exactly this JSON structure:

{
    "summary": "",
    "possible_conditions": [
        {
            "name": "",
            "reason": ""
        }
    ],
    "urgency_level": "",
    "recommended_next_steps": [],
    "questions_for_doctor": [],
    "warning_signs": []
}

The urgency_level must be exactly one of:
LOW, MEDIUM, HIGH, EMERGENCY.
"""


# ---------------------------------------------------------
# PromptTemplate
# ---------------------------------------------------------

MEDICAL_PROMPT = """
Patient age: {age}
Gender: {gender}

Symptoms:
{symptoms}

Duration:
{duration}

Severity: {severity}/10

Existing medical conditions:
{conditions}

Current medications:
{medications}

Additional notes:
{notes}

Answer language:
{language}

Provide safe, educational preliminary guidance based on the
information above.

{json_schema}
"""


prompt_template = PromptTemplate(
    input_variables=[
        "age",
        "gender",
        "symptoms",
        "duration",
        "severity",
        "conditions",
        "medications",
        "notes",
        "language",
        "json_schema"
    ],
    template=MEDICAL_PROMPT
)


# ---------------------------------------------------------
# ChatPromptTemplate
# ---------------------------------------------------------

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """
Patient information:

Age: {age}
Gender: {gender}

Symptoms:
{symptoms}

Duration:
{duration}

Severity: {severity}/10

Existing medical conditions:
{conditions}

Current medications:
{medications}

Additional notes:
{notes}

Answer language:
{language}

{json_schema}
""")
])


# ---------------------------------------------------------
# Narrative prompt for streaming
# ---------------------------------------------------------

NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """
You are MediGuide AI.

Provide a short, clear, educational explanation of the patient's
information.

You are NOT a doctor and must not give a confirmed diagnosis.
Encourage consultation with a qualified healthcare professional.
If the situation appears urgent, advise seeking emergency medical
help immediately.

Respond in the requested language.
"""),
    ("human", """
Patient information:

Age: {age}
Gender: {gender}
Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}/10
Existing conditions: {conditions}
Medications: {medications}
Additional notes: {notes}

Answer language: {language}
""")
])