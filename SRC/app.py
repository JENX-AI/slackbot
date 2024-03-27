# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
import together

#=====================================
# Credentials
#=====================================

load_dotenv("../.env")
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
together.api_key = os.environ["TOGETHER_API_KEY"]

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)

#=====================================
# Direct message handler for Slack
#=====================================
@app.message(".*")
def message_handler(message, say, logger):
    user_message = message['text']  # Extract the user's message from the Slack event

    # Provide background context for the LLM for generating responses
    context_prompt = (
        """
        Just be a general purpose LLM. Use professional corporate language.
        """
    )
    query = user_message
    # Provide specific information for the LLM to base the comment off of
    specific_prompt = [
        f"Answer the specific prompt: {user_message}"
    ]   

    # Construct the final prompt for the LLM based off of the context_prompt and specific_prompt
    prompt = f"<s>[INST] <<SYS>>{context_prompt}<</SYS>>\\n\\n"

    for specifics in specific_prompt:
        prompt += f"[INST]{specifics}[/INST]"

    try:
        output = together.Complete.create(
            prompt,
            model="togethercomputer/llama-2-13b-chat",
            max_tokens=1000,
            temperature=0.1,
            top_k=90,
            top_p=1.0,
            repetition_penalty=1.1,
            stop=['</s>']
        )
        complete_output = output['output']['choices'][0]['text']
    except Exception as e:
        complete_output = f"Error: {e}. \n\nPlease make sure your API key below is correct and valid."

    say(complete_output)  # Send the generated response back to Slack


@app.event(("app_mention"))
def handle_app_mention_events(body, say, logger):
    user_message = body['event']['text']  # Extract the user's message from the Slack event

    # Provide background context for the LLM for generating responses
    context_prompt = (
        """
        Just be a general purpose LLM. Use professional corporate language.
        """
    )
    query = user_message
    # Provide specific information for the LLM to base the comment off of
    specific_prompt = [
        f"Answer the specific prompt: {user_message}"
    ]   

    # Construct the final prompt for the LLM based off of the context_prompt and specific_prompt
    prompt = f"<s>[INST] <<SYS>>{context_prompt}<</SYS>>\\n\\n"

    for specifics in specific_prompt:
        prompt += f"[INST]{specifics}[/INST]"

    try:
        output = together.Complete.create(
            prompt,
            model="togethercomputer/llama-2-13b-chat",
            max_tokens=1000,
            temperature=0.1,
            top_k=90,
            top_p=1.0,
            repetition_penalty=1.1,
            stop=['</s>']
        )
        complete_output = output['output']['choices'][0]['text']
    except Exception as e:
        complete_output = f"Error: {e}. \n\nPlease make sure your API key below is correct and valid."

    say(complete_output)  # Send the generated response back to Slack


#==============================

if __name__ == "__main__":
    # Create an app-level token with connections:write scope
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()