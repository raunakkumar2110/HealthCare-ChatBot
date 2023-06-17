import streamlit as st
import openai

# Set up your OpenAI API credentials
openai.api_key = st.secrets['pass']

# Title and input prompt
st.title("Healthcare Chatbot")

# Capture basic patient details
name = st.text_input("Patient Name:")
age = st.number_input("Patient Age:")
gender = st.selectbox("Patient Gender:", ["Male", "Female", "Other"])

# User query input
user_input = st.text_input("Ask a question:")

# Initialize an empty list to store previous responses and patient details
previous_responses = []
patient_details = {"Name": name, "Age": age, "Gender": gender}

# Function to generate response
def generate_response(question, conversation):
    # Check if the question is a greeting
    if is_greeting(question):
        return f"Hello {patient_details['Name']}! I'm a healthcare chatbot. How can I assist you today?"

    # Filter out non-healthcare queries
    if not is_healthcare_related(question):
        return "Please ask a healthcare-related question."
    
    # Append the user's question to the conversation
    conversation.append("User: " + question)

    # Send the conversation history to the GPT-3 model
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="\n".join(conversation),
        max_tokens=100,
        temperature=0.2,
        n=1,
        stop=None,
        echo=False,
    )

    # Extract the generated answer from the GPT-3 response
    answer = response.choices[0].text.strip()

    # Append the generated answer to the conversation
    conversation.append("Chatbot: " + answer)

    return answer

# Function to check if a question is a greeting
def is_greeting(question):
    # Define a list of greeting keywords
    greeting_keywords = ["hello", "hi", "hey", "hii", "who are you"]

    # Check if the question starts with any of the keywords
    for keyword in greeting_keywords:
        if question.lower().startswith(keyword):
            return True

    return False

# Function to determine if a question is healthcare-related
def is_healthcare_related(question):
    # Define a list of healthcare-related keywords
    healthcare_keywords = [
        "health", "medical", "doctor", "hospital", "treatment", "medicine",
        "patient","ok","great","how are you","feeling","helpless","doctor"
    ]  # just for now we have done this else we can use NER and other methods

    # Check if any of the keywords are present in the question
    for keyword in healthcare_keywords:
        if keyword in question.lower():
            return True

    return False

# Generate response
if st.button("Get Answer"):
    # Generate response based on the user's question and the conversation history
    response = generate_response(user_input, previous_responses)

    # Store the conversation history
    previous_responses.append("User: " + user_input)
    previous_responses.append("Chatbot: " + response)

    st.text_area("Chatbot Response:", response, height=200)

st.image('chatic.png', width=300)
