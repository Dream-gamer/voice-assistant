import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import base64

#Init openai client
def setup_openai_client(api_key):

    return openai.OpenAI(api_key=api_key)

# Transcribe audio to text

def transcribe_audio(client, audio_path):

    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model = "whisper-1", file = audio_file)
        return transcript.text
    
# Taking response from Openai
def fetch_ai_response(client, input_text):
    messages = [{"role":"user","content":input_text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].messages.content

def text_to_audio(client, text, audio_path):
    response = client.audio.speech.create(model="tts-1",voice="nova",input=text)
    response.stream_to_file(audio_path)

def main():

    st.sidebar.title("API KEY CONFIG")
    api_key=st.sidebar.text_input("Enter your OpenAI API key", type="password")

    st.title("EHR query assistant")
    st.write("Hi there! Click on the voice recorder to interact with me.")
    
    # check if api key is there
    # if api_key:
    client = setup_openai_client(api_key)
    recorded_audio=audio_recorder()
    # check if rec done and available
    if recorded_audio:
        audio_file = "audio.mp3"
        with open(audio_file, "wb") as f:
            f.write(recorded_audio)

        transcribed_text = transcribe_audio(client, audio_file)
        st.write("Transcribed Text: ", transcribed_text)

        ai_response = fetch_ai_response(client, transcribed_text)
        st.write("AI response: ", ai_response)

if __name__ == "__main__":
    main()