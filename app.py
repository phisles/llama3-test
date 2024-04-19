import streamlit as st
import requests
import json
import textwrap

def process_chunk(chunk):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama3",
        "stream": False,
        "prompt": "Please summarize the following text: " + chunk
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        return data["response"]
    else:
        return "Error: " + str(response.status_code)

st.title('Transcript Summarizer')

transcript = st.text_area("Paste the transcript here:", height=300)

if st.button('Summarize Transcript'):
    words = transcript.split()
    word_count = len(words)
    st.write(f"Total words: {word_count}")

    if word_count > 2500:
        chunks = textwrap.wrap(transcript, 500)
        st.write(f"Number of chunks: {len(chunks)}")
        responses = []
        for i, chunk in enumerate(chunks):
            st.write(f"Processing chunk {i+1}/{len(chunks)}...")
            response = process_chunk(chunk)
            responses.append(response)
            st.write("Chunk processed.")
        combined_response = " ".join(responses)
        st.text_area("Summarized Response:", value=combined_response, height=300)
    else:
        response = process_chunk(transcript)
        st.text_area("Summarized Response:", value=response, height=300)
