
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

ASSISTANT_NAME = "AI Tutor"
ASSISTANT_INSTRUCTIONS = "You are a helpful AI tutor. Explain concepts clearly and provide step-by-step solutions."

def create_or_retrieve_assistant(name=ASSISTANT_NAME, instructions=ASSISTANT_INSTRUCTIONS, model="gpt-4o"):
    """
    Creates a new assistant or retrieves an existing one by name.
    """
    try:
        my_assistants = client.beta.assistants.list(order="desc", limit="20")
        for assistant in my_assistants.data:
            if assistant.name == name:
                print(f"Retrieved existing assistant: {assistant.id} - {assistant.name}")
                return assistant

        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
            tools=[{"type": "code_interpreter"}],
        )
        print(f"Created new assistant: {assistant.id} - {assistant.name}")
        return assistant
    except Exception as e:
        print(f"An error occurred in create_or_retrieve_assistant: {e}")
        return None

def create_thread():
    """
    Creates a new thread.
    """
    try:
        thread = client.beta.threads.create()
        print(f"Created new thread: {thread.id}")
        return thread
    except Exception as e:
        print(f"An error occurred in create_thread: {e}")
        return None

def add_message_to_thread(thread_id, user_message):
    """
    Adds a user message to a thread.
    """
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message,
        )
        print(f"Added message to thread: {message.id}")
        return message
    except Exception as e:
        print(f"An error occurred in add_message_to_thread: {e}")
        return None

def run_assistant_on_thread(thread_id, assistant_id):
    """
    Runs the assistant on the specified thread.
    """
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        print(f"Started run: {run.id}")
        return run
    except Exception as e:
        print(f"An error occurred in run_assistant_on_thread: {e}")
        return None

def wait_for_run_completion(thread_id, run_id):
    """
    Polls the run status until it completes.
    """
    import time
    while True:
        try:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            print(f"Run status: {run_status.status}")
            if run_status.status in ['completed', 'failed', 'cancelled', 'expired']:
                return run_status
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred in wait_for_run_completion: {e}")
            return None

def get_assistant_response(thread_id):
    """
    Retrieves the assistant's messages from the thread.
    """
    try:
        messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
        return messages
    except Exception as e:
        print(f"An error occurred in get_assistant_response: {e}")
        return None
