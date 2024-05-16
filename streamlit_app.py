import streamlit as st
import requests
import json

# pip install streamlit requests

# Function to send data to the API
def send_to_api(text):
    OPENROUTER_API_KEY = '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'  # Replace with your OpenRouter API key
    #YOUR_SITE_URL = 'http://your-site-url.com'  # Optional, replace with your site URL
    #YOUR_APP_NAME = 'YourAppName'  # Optional, replace with your app name

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                #"HTTP-Referer": YOUR_SITE_URL,
                #"X-Title": YOUR_APP_NAME,
            },
            data=json.dumps({
                "model": "google/gemma-7b-it",  # Optional
                "messages": [
                    {"role": "user", "content": text}
                ]
            })
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Failed to fetch data from API', 'status_code': response.status_code}
    except Exception as e:
        return {'error': str(e)}

# Streamlit UI components
st.title('Common Belief')

main_text = "Why is male an important predictor?"

# Text input for main text
main_text = st.text_area("Insert question here:", main_text)

additional_info_text = """This is information from a machine learning model trained on the Titanic dataset.

Feature_Importance = {
    Sex_male: 0.0608, 
    Sex_female: 0.0572, 
    Pclass: 0.0456,
    Fare: 0.0103,
    Embarked_S: 0.0061,
    SibSp: 0.0036,
    Parch: 0.0016,
    Embarked_C: 0.0004,
    Embarked_Q: 0.0002}"""

# Text input for additional information
additional_info = st.text_area("Insert background information here:", additional_info_text, height=300)

# Send button
if st.button('Send'):
    combined_text = f"You are a data analyst that answers questions based on a trained machine learning model. In the following, you get access to the feature importance of the machine learning model and then will be asked a question. Answer the question based on the feature importance.\n\n{additional_info}\nQuestion: {main_text}"
    api_response = send_to_api(combined_text)
    if 'error' in api_response:
        st.error(f"Error: {api_response['error']}")
    else:
        st.success("Success! Response from API:")
        st.json(api_response)
