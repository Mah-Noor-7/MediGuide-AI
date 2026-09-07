# MediGuide AI

MediGuide AI is an educational medical information assistant built with Python and Streamlit. It provides users with general health and medical information through an interactive AI-powered interface.

## Features

* AI-powered medical information assistant
* Interactive Streamlit interface
* Educational health and medical information
* Structured responses for better readability
* Environment-based API key configuration
* SQLite-based caching support

## Technologies Used

* Python
* Streamlit
* LangChain
* OpenAI API
* SQLite
* python-dotenv

## Project Structure

```text
medical_ai_assistant/
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── chains.py
│   ├── config.py
│   ├── prompts.py
│   └── utils.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Mah-Noor-7/MediGuide-AI.git
cd MediGuide-AI
```

Create and activate a virtual environment:

```bash
py -m venv venv
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add your API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not upload your `.env` file or API key to GitHub.

## Run the Application

Start the Streamlit application with:

```bash
py -m streamlit run src/app.py
```

The application will open in your browser.

## Disclaimer

MediGuide AI is designed for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Users should consult a qualified healthcare professional for medical concerns.

## Author

Mah Noor

GitHub: https://github.com/Mah-Noor-7
