import streamlit as st
import os
from src.cache_manager import use_sqlite_cache
from src.config import (
    GENDER_OPTIONS,
    DURATION_OPTIONS,
    LANGUAGE_OPTIONS
)

from src.chains import run_assessment
from src.utils import safe_json_parse, validate_assessment


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

use_sqlite_cache()

st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🩺",
    layout="wide"
)


# ---------------------------------------------------------
# API Key Setup
# ---------------------------------------------------------
# Ask the user for their own API key before showing the
# patient-information interface.
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if not st.session_state.api_key:
    st.title("🩺 MediGuide AI")
    st.subheader("🔑 Enter your API Key")

    st.info(
        "Please enter your own API key to use MediGuide AI. "
        "Your key is used only for the current Streamlit session."
    )

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="Enter your API key here..."
    )

    if st.button("Continue →", type="primary"):
        if not api_key.strip():
            st.warning("Please enter your API key first.")
        else:
            st.session_state.api_key = api_key.strip()
            os.environ["OPENAI_API_KEY"] = st.session_state.api_key
            st.rerun()

    st.stop()

# Make the key available to the LangChain/OpenAI code.
os.environ["OPENAI_API_KEY"] = st.session_state.api_key


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🩺 MediGuide AI")
st.subheader("Educational Medical Information Assistant")

st.info(
    "MediGuide AI provides educational information only. "
    "It is not a doctor, does not provide a confirmed diagnosis, "
    "and does not replace professional or emergency medical care."
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.header("MediGuide AI")

    if st.button("🔄 Change API Key"):
        st.session_state.api_key = ""
        os.environ.pop("OPENAI_API_KEY", None)
        st.rerun()

    st.write(
        "An AI assistant for educational medical information."
    )

    st.markdown("---")

    st.subheader("⚠️ Safety Notice")

    st.write(
        "For emergencies or severe symptoms, "
        "seek professional medical help immediately."
    )


# ---------------------------------------------------------
# Patient Information
# ---------------------------------------------------------

st.header("👤 Patient Information")

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

    gender = st.selectbox(
        "Gender",
        GENDER_OPTIONS
    )


with col2:

    duration = st.selectbox(
        "Symptom Duration",
        DURATION_OPTIONS
    )

    severity = st.slider(
        "Symptom Severity",
        min_value=1,
        max_value=10,
        value=5
    )


# ---------------------------------------------------------
# Symptoms
# ---------------------------------------------------------

st.header("🩺 Symptoms")

symptoms = st.text_area(
    "Describe your symptoms",
    placeholder="Example: headache, fever, cough...",
    height=120
)


# ---------------------------------------------------------
# Medical History
# ---------------------------------------------------------

st.header("📋 Medical History")

conditions = st.text_area(
    "Existing medical conditions",
    placeholder="Example: asthma, diabetes, none...",
    height=80
)

medications = st.text_area(
    "Current medications",
    placeholder="List any current medications...",
    height=80
)

notes = st.text_area(
    "Additional notes",
    placeholder="Anything else you want the assistant to know...",
    height=80
)


# ---------------------------------------------------------
# Language
# ---------------------------------------------------------

language = st.selectbox(
    "🌐 Response Language",
    LANGUAGE_OPTIONS
)


# ---------------------------------------------------------
# AI Assessment
# ---------------------------------------------------------

if st.button(
    "🔍 Get Educational Guidance",
    type="primary"
):

    if not symptoms.strip():

        st.warning(
            "Please describe your symptoms before submitting."
        )

    else:

        inputs = {
            "age": age,
            "gender": gender,
            "symptoms": symptoms,
            "duration": duration,
            "severity": severity,
            "conditions": conditions,
            "medications": medications,
            "notes": notes,
            "language": language,
            "json_schema": """
Return JSON with these fields:

summary,
possible_conditions,
urgency_level,
recommended_next_steps,
questions_for_doctor,
warning_signs
"""
        }

        with st.spinner(
            "MediGuide AI is preparing educational guidance..."
        ):

            try:

                # Call LangChain
                raw_response = run_assessment(inputs)

                # Convert response to dictionary
                result = safe_json_parse(raw_response)

                # Validate response
                if not validate_assessment(result):

                    st.error(
                        "The AI returned an unexpected response format."
                    )

                else:

                    st.success(
                        "Educational guidance generated successfully."
                    )

                    # -------------------------------------------------
                    # Assessment Results
                    # -------------------------------------------------

                    st.header("📊 Assessment Results")


                    # -------------------------------------------------
                    # Summary
                    # -------------------------------------------------

                    st.subheader("Summary")

                    st.write(
                        result["summary"]
                    )


                    # -------------------------------------------------
                    # Possible Conditions
                    # -------------------------------------------------

                    st.subheader("Possible Conditions")

                    conditions_result = result["possible_conditions"]

                    if isinstance(conditions_result, str):

                        st.write(conditions_result)

                    else:

                        for condition in conditions_result:

                            if isinstance(condition, dict):

                                st.markdown(
                                    f"**{condition.get('name', 'Unknown')}**"
                                )

                                st.write(
                                    condition.get("reason", "")
                                )

                            else:

                                st.write(
                                    f"• {condition}"
                                )


                    # -------------------------------------------------
                    # Urgency Level
                    # -------------------------------------------------

                    st.subheader("Urgency Level")

                    urgency = result["urgency_level"]

                    if urgency == "EMERGENCY":

                        st.error(
                            "🚨 EMERGENCY — Please seek emergency "
                            "medical care immediately."
                        )

                    elif urgency == "HIGH":

                        st.warning(
                            "⚠️ HIGH — Please seek professional "
                            "medical advice promptly."
                        )

                    elif urgency == "MEDIUM":

                        st.warning(
                            "MEDIUM — Consider consulting a "
                            "healthcare professional."
                        )

                    else:

                        st.info(
                            "LOW — Monitor your symptoms and "
                            "consider professional advice if they persist."
                        )


                    # -------------------------------------------------
                    # Recommended Next Steps
                    # -------------------------------------------------

                    st.subheader("Recommended Next Steps")

                    steps = result["recommended_next_steps"]

                    if isinstance(steps, str):

                        st.write(steps)

                    else:

                        for step in steps:

                            st.write(
                                f"• {step}"
                            )


                    # -------------------------------------------------
                    # Questions for Doctor
                    # -------------------------------------------------

                    st.subheader("Questions for Your Doctor")

                    questions = result["questions_for_doctor"]

                    if isinstance(questions, str):

                        st.write(questions)

                    else:

                        for question in questions:

                            st.write(
                                f"• {question}"
                            )


                    # -------------------------------------------------
                    # Warning Signs
                    # -------------------------------------------------

                    st.subheader("⚠️ Warning Signs")

                    warnings = result["warning_signs"]

                    if isinstance(warnings, str):

                        st.write(warnings)

                    else:

                        for warning in warnings:

                            st.write(
                                f"• {warning}"
                            )


                    # -------------------------------------------------
                    # Disclaimer
                    # -------------------------------------------------

                    st.caption(
                        "This information is educational only and "
                        "is not a medical diagnosis."
                    )


            except Exception as error:

                st.error(
                    "Something went wrong while processing the request."
                )

                st.exception(error)