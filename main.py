import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("AIzaSyApriC9INk_Yia9ZFMkfLUSK53cmb6jrFg")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("Legal Ease - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH",
  },
]

model = gen_ai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="You are a Sam, Law expert who specializes in designating proper IPCs to the offenses listed by the user. The IPCs should be based on Indian Law. You are aiding the Law enforcement agencies, so do not mention reporting the incident to the law agencies. Also, put a little disclaimer at the bottom about double checking the output. You must provide the most applicable IPC section and give the reasons why. On top of that, give some alternatives as to what other IPC sections may be applicable under certain conditions",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Help me categorize criminal offences under different IPC sections. Ask for specifics if required. Though, keep the questions specific as well",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I can definitely help you categorize criminal offences under different IPC sections. Please tell me about the offense you are looking to classify. To help me give you the most accurate IPC section, please provide details about:\n\n1. *Nature of the offense:* What type of act is involved? (e.g., theft, assault, murder, fraud, etc.)\n2. *Circumstances of the offense:* What happened? Please provide as much detail as you can about the context, the actions involved, and any other relevant information. \n3. *Intent of the offender:* Did the offender intentionally commit the offense, or was it negligent or accidental? \n\nThe more information you provide, the better I can guide you to the most appropriate IPC section. \n\n*Disclaimer:* I am an AI chatbot and not a legal professional. This information is for informational purposes only and should not be considered legal advice. You should consult with a qualified attorney for legal advice. \n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)
print(chat_session.history)