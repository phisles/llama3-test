import streamlit as st
import requests
import json
import time

def process_chunk(chunk):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    
    prompt_text = (
        "You are a police analyst reviewing transcripts from police interviews and body worn cameras. "
        "Please provide a concise and factual summary of no more than 100 words of this transcript, "
        "focusing on key events and interactions. Highlight any critical incidents, notable exchanges, and official actions taken by the officer. "
        "Ensure the summary is clear and neutral, maintaining an objective tone throughout. "
        "If the transcript is in another language, provide your summary in English. "
        "If the quality of the transcript is hard to interpret, it is because the audio quality is poor. In such scenarios, do the best you can to interpret the transcript."
    )
    
    full_prompt = prompt_text + chunk  # Combine the fixed prompt with the chunk of text

    data = {
        "model": "llama3",
        "stream": False,
        "prompt": full_prompt
    }
    
    start_time = time.time()  # Start timing before the request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    processing_time = time.time() - start_time  # End timing after the request
    
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        return data["response"], processing_time  # Return both the response and the processing time
    else:
        return "Error: " + str(response.status_code), processing_time  # Include processing time even in case of error

st.title('Llama3 Transcript Summerizer')
st.subheader('Breaks transcript into chunks of 2500 characters, summarizes, combines these summaries, then generates a summary of the combined summaries')
transcript = st.text_area("Paste the transcript here:", height=300)

if st.button('Summarize Transcript'):
    start_overall_time = time.time()
    characters_in_transcript = len(transcript)
    words_in_transcript = len(transcript.split())
    chunks = [transcript[i:i+2500] for i in range(0, len(transcript), 2500)]
    
    summaries = []
    chunk_times = []
    chunk_characters_counts = []
    chunk_words_counts = []

    with st.container():
        main_col, summary_col = st.columns([2, 1])
        
        with main_col:
            st.markdown(f"<div style='color: yellow;'>Original Transcript: {words_in_transcript} Words / {characters_in_transcript} Characters</div>", unsafe_allow_html=True)
        
        with summary_col:
            st.write("**Summary Data**", unsafe_allow_html=True)
            st.write(f"**<font color='yellow'>Total Word Count:</font>** {words_in_transcript}", unsafe_allow_html=True)
            st.write(f"**<font color='yellow'>Total Character Count:</font>** {characters_in_transcript}", unsafe_allow_html=True)
            st.write(f"**<font color='blue'>Number of Chunks:</font>** {len(chunks)}", unsafe_allow_html=True)



        for i, chunk in enumerate(chunks):
            response, processing_time = process_chunk(chunk)
            chunk_characters = len(chunk)
            chunk_words = len(chunk.split())
            summaries.append(response)
            chunk_times.append(processing_time)
            chunk_characters_counts.append(chunk_characters)
            chunk_words_counts.append(chunk_words)

            with main_col:
                st.markdown(f"<div style='color: blue; margin-left: 20px;'>**Chunk {i+1} Summary Preview:** {response[:200] + '...' if len(response) > 200 else response} (Processed in {processing_time:.2f} seconds)</div>", unsafe_allow_html=True)
            
            with summary_col:
                st.write(f"**<font color='blue'>Chunk {i+1}:**</font> {chunk_words} Words, {chunk_characters} Characters, {processing_time:.2f} sec", unsafe_allow_html=True)

    combined_response = " ".join(summaries).replace('\n', ' ').replace('\r', '')
    total_characters = sum(len(response) for response in summaries)
    response_placeholder = st.text_area("Summarized Response:", value=combined_response, height=300, key='combined')
    st.write(f"**Total characters in summarized response:** {total_characters}")

    final_prompt = ("You are an investigator reviewing combined summaries of an audio transcript. "
                    "You will receive a large text file containing multiple summaries of different parts of the transcript. "
                    "If the combined summary introduces another summary, it is the same summary, and should be considered an extension of the first summary"
                    "You will summarize these summaries, removing any extraneous content such as what the text contains or audio quality issues, or duplicated details. "
                    "You will then provide the final summary as a concise summary that does not add any description other than the summary itself. "
                    "Your response will only contain the summary. Exclude introductory phrases in your response such as 'Here is a concise and factual summary of the  transcript, or Here is...'"
                    "Here is the combined summary text to summarize:")
    final_full_prompt = final_prompt + combined_response
    final_summary, final_processing_time = process_chunk(final_full_prompt)
    end_overall_time = time.time()
    total_time = end_overall_time - start_overall_time

    with summary_col:
        st.markdown(f"**<font color='red'>Final Summary Processing Time:</font>** {final_processing_time:.2f} seconds", unsafe_allow_html=True)
        st.markdown(f"**<font color='purple'>Total Processing Time:</font>** {total_time:.2f} seconds", unsafe_allow_html=True)



    response_placeholder = st.text_area("Final Summarized Response:", value=final_summary, height=300, key='final')

    # Download button
    if st.button('Download Final Summarized Text'):
        st.download_button(
            label="Download Text",
            data=final_summary,
            file_name='final_summarized_transcript.txt',
            mime='text/plain'
        )

