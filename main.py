import ollama
import pyttsx3
import streamlit as st
tts_engine = pyttsx3.init()

# Define a function to convert text to speech
def text_to_speech(text):
    global tts_engine  # Access the global TTS engine
    tts_engine.say(text)
    tts_engine.startLoop(False)  # Ensure the loop is not already running
    tts_engine.iterate()  # Process the speech queue
    tts_engine.endLoop() 


def clear_chat_history():
    st.session_state.messages = []

def main():
    
    st.set_page_config(page_title="🦙💬 Medical Chatbot")
    
    with st.sidebar:
        st.title('🦙💬 Medical Chatbot') 
        st.markdown('📖 Ask your queries to the llama-powered Medical Chatbot')
    
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
    
    st.title("Medical Chatbot")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])
    
    query = st.chat_input("Ask your query here")

    if query:
        st.chat_message('user').markdown(query)
        st.session_state.messages.append({'role':'user','content':query})
        response = final_result(query)
        response_str = response
        st.chat_message('assistant').markdown(response)
        text_to_speech(response)
        st.session_state.messages.append({'role':'assistant','content':response_str})


def final_result(query):
    response = ollama.chat(model='medllama2', messages=[{'role': 'user','content': query,}])
    return response['message']['content']


if __name__ == "__main__":
    main()