# -*- coding: utf-8 -*-
import os, logging
from dotenv import load_dotenv
import slack_bolt
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
import together

# Constants
from config import SYSTEM_PROMPT, MODEL, MAX_TOKENS, TEMPERATURE
from config import TOP_K, TOP_P, REPETITION_PENALTY
# Credentials
load_dotenv("../.env")
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
together.api_key = os.environ["TOGETHER_API_KEY"]

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)

# ====================================
# Direct message handler for Slack
# ====================================

@app.message(".*")
def message_handler(message: dict, say: slack_bolt.Say, logger: logging.Logger) -> None:
    """
    Handles messages to chatbot within Apps
    
    Parameters
    ----------
    message : dict
        message received from Slack user in Apps
    
    say : slack_bolt.Say
        sends message to Slack
    
    logger : logging.Logger
        logging object
    """
    # Extract user message from Slack event
    user_message = message["text"]  
    # Construct final prompt for LLM based on SYSTEM_PROMPT and specific_prompt
    prompt = f"<s>[INST] <<SYS>>{SYSTEM_PROMPT}<</SYS>>\\n\\n"
    # prompt += f"[INST]{specific_prompt}[/INST]"
    prompt += f"[INST] Answer the user prompt: {user_message}[/INST]"

    try:
        output = together.Complete.create(
            prompt,
            model=MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE, 
            top_k=TOP_K, top_p=TOP_P, repetition_penalty=REPETITION_PENALTY,
            stop=["</s>"]
        )
        complete_output = output["output"]["choices"][0]["text"]
    
    except Exception as e:
        complete_output = f"Error: {e}. \n\nPlease make sure your API key below is correct and valid."
    
    # Send the generated response back to Slack
    say(complete_output)  


@app.event(("app_mention"))
def handle_app_mention_events(body: dict, say: slack_bolt.Say, logger: logging.Logger) -> None:
    """
    Handles direct (@) messages to chatbot within Channels
    
    Parameters
    ----------
    body : dict
        message received from Slack user in Channels
    
    say : slack_bolt.Say
        sends message to Slack
    
    logger : logging.Logger
        logging object
    """
    # Extract user message from Slack event
    user_message = body["event"]["text"]
    # Construct final prompt for LLM based on SYSTEM_PROMPT and specific_prompt
    prompt = f"<s>[INST] <<SYS>>{SYSTEM_PROMPT}<</SYS>>\\n\\n"
    # prompt += f"[INST]{specific_prompt}[/INST]"
    prompt += f"[INST] Answer the user prompt: {user_message}[/INST]"

    try:
        output = together.Complete.create(
            prompt,
            model=MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE, 
            top_k=TOP_K, top_p=TOP_P, repetition_penalty=REPETITION_PENALTY,
            stop=["</s>"]
        )
        complete_output = output["output"]["choices"][0]["text"]
    
    except Exception as e:
        complete_output = f"Error: {e}. \n\nPlease make sure your API key below is correct and valid."
    
    # Send the generated response back to Slack
    say(complete_output)  


# ====================================
# Initialisation
# ====================================

if __name__ == "__main__":
    # Create an app-level token with connections:write scope
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
