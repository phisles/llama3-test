## Summary

This code utilizes the Streamlit framework to create a web application for summarizing transcripts using an AI model. **Before running this application, ensure that you have [Ollama](https://ollama.com/) installed and the application is running to ensure localhost is active**; the application interacts with Ollama to utilize the Llama3 model.

Here's a summary of what it does and how it works:

1. **User Input**: Users paste a transcript into a text area on the web interface.
2. **Chunking**: The transcript is divided into chunks of 2500 characters each.
3. **Processing Each Chunk**: Each chunk is sent to an API endpoint (`http://localhost:11434/api/generate`) along with a fixed prompt for summarization. The API uses the Llama3 model via Ollama. The response and processing time for each chunk are recorded.
4. **Displaying Chunk Summaries**: The summarized text for each chunk, along with its word count, character count, and processing time, is displayed on the web interface.
5. **Combining Summaries**: The individual chunk summaries are combined into a single text, and extraneous content is removed.
6. **Final Summary**: The combined summary is sent to the API again for further summarization, and the final summarized response is displayed along with its processing time.
7. **Download**: Users can download the final summarized text as a file, with summary details included.

The code mainly interacts with the Streamlit framework for the user interface, makes requests to an external API for text summarization using the Llama3 model via Ollama, processes the received data, and displays it back to the user.
