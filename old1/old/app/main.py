
import streamlit as st
import assistant

# --- Page Setup ---
st.set_page_config(page_title="AI Tutor", page_icon="🤖", layout="wide")

st.title("AI Tutor 🤖")
st.caption("A helpful AI tutor powered by OpenAI's Assistants API")

# --- Assistant and Thread Initialization ---
if 'assistant' not in st.session_state:
    st.session_state.assistant = assistant.create_or_retrieve_assistant()

if 'thread' not in st.session_state:
    st.session_state.thread = assistant.create_thread()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Chat Display ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Add message to the thread
    assistant.add_message_to_thread(st.session_state.thread.id, prompt)

    # Run the assistant
    run = assistant.run_assistant_on_thread(st.session_state.thread.id, st.session_state.assistant.id)

    # Wait for the run to complete
    with st.spinner("Thinking..."):
        run = assistant.wait_for_run_completion(st.session_state.thread.id, run.id)

    if run and run.status == 'completed':
        # Get the assistant's response
        messages = assistant.get_assistant_response(st.session_state.thread.id)
        if messages:
            for message in messages:
                if message.role == "assistant":
                    # Find the latest assistant message
                    for content_block in message.content:
                        if content_block.type == 'text':
                            latest_response = content_block.text.value
                            # Check if the message is not already displayed
                            if not any(msg["content"] == latest_response and msg["role"] == "assistant" for msg in st.session_state.messages):
                                st.session_state.messages.append({"role": "assistant", "content": latest_response})
                                st.chat_message("assistant").write(latest_response)

    else:
        st.error("The assistant failed to respond.")

