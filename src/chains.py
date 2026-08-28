from langchain_openai import ChatOpenAI
from langchain_classic.chains import LLMChain

from src.config import OPENAI_API_KEY, MODEL_NAME
from src.prompts import chat_prompt_template


# ---------------------------------------------------------
# Create OpenAI Chat Model
# ---------------------------------------------------------

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME,
    temperature=0
)


# ---------------------------------------------------------
# Create reusable LLMChain
# ---------------------------------------------------------

medical_chain = LLMChain(
    llm=llm,
    prompt=chat_prompt_template
)


# ---------------------------------------------------------
# Run medical assessment
# ---------------------------------------------------------

def run_assessment(inputs):
    """
    Send patient information to the LangChain chain
    and return the AI response.
    """

    response = medical_chain.invoke(inputs)

    return response["text"]


# ---------------------------------------------------------
# Streaming function
# ---------------------------------------------------------

def stream_narrative(llm_model, inputs):
    """
    Stream the AI-generated narrative response
    chunk by chunk.
    """

    messages = chat_prompt_template.format_messages(**inputs)

    for chunk in llm_model.stream(messages):
        if chunk.content:
            yield chunk.content