# -*- coding: utf-8 -*-
import os, logging, re
from dotenv import load_dotenv
import slack_bolt
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain_together import Together

# Constants
from config import SYSTEM_PROMPT, MODEL, MAX_TOKENS, TEMPERATURE
from config import TOP_K, TOP_P, REPETITION_PENALTY
# Credentials
load_dotenv("../.env")
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
TOGETHER_API_KEY = os.environ["TOGETHER_API_KEY"]

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)

# ====================================
# LLM Model
# ====================================

# Master dict to store different discussions
THREADS_DICT = dict()

LLM_MODEL = Together(
        model=MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_k=TOP_K,
        top_p=TOP_P,
        repetition_penalty=REPETITION_PENALTY,
        together_api_key=TOGETHER_API_KEY
    )

# ====================================
# String formatting
# ====================================

def regex_whitespace(raw_text: str) -> str:
    """
    Converts whitespace characters to regular spaces
    Called by add_chain_link()
    """
    # Replace all whitespace with single space
    clean_text = re.sub(r"\s+", " ", raw_text)
    # Remove leading and trailing whitespace
    clean_text = clean_text.strip()
    # Remove "AI:" and "AI Assistant:" prefixes
    clean_text = re.sub(r"^(AI\:|\s+AI Assistant\:)(.*)", r"\2", clean_text)
    
    return clean_text
    
    
def regex_slack_id(raw_text: str) -> str:
    """
    Removes Slack user ID from start of message (if applicable)
    Called by add_chain_link()
    """
    # Slack user ID format (optional colon and whitespace)
    pattern = r"^([A-Z0-9_]{9,11}):?\s*"  
    match = re.match(pattern, raw_text)
    if match:
        # Return remaining raw_text after user ID
        return raw_text[match.end():]  
    # Return original raw_text if no user ID found
    return raw_text  
    
    
# ====================================
# ConversationChain
# ====================================

def build_chain(thread_id: str) -> None:
    """
    Creates conversation chain upon first mention of bot
    Called by message_handler()
    """
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=SYSTEM_PROMPT)
    
    memory = ConversationSummaryBufferMemory(llm=LLM_MODEL, max_token_limit=MAX_TOKENS)
    
    chain = ConversationChain(
        prompt=PROMPT,
        llm=LLM_MODEL,
        verbose=True,
        memory=memory
    )
    # Add ConversationChain to dict
    THREADS_DICT[thread_id] = {
        "memory": memory, 
        "chain": chain
    }
    

def add_chain_link(thread_id: str, msg: dict, loc: str) -> str:
    """
    Adds ConversationChain link for latest message round
    Called by message_handler()
    """
    # Extract user message from Slack event
    if loc == "apps":
        # msg_author = msg["user"]
        msg_txt = regex_whitespace(msg["text"])
        # msg_content = f"{msg_author}: {msg_txt}"
    
    elif loc == "mentions":
        # msg_author = msg["event"]["user"]
        msg_txt = regex_whitespace(msg["event"]["text"])
        # msg_content = f"{msg_author}: {msg_txt}"
    
    try:
        # bot_msg = THREADS_DICT[thread_id]["chain"].predict(input=msg_content)
        bot_msg = THREADS_DICT[thread_id]["chain"].predict(input=msg_txt)
        # Clean messages with regex
        rgx_msg = regex_slack_id(bot_msg)
        rgx_msg = regex_whitespace(rgx_msg)
        
        return rgx_msg
    
    except KeyError as e:
        logger.error(f"KeyError for THREADS_DICT: {e}")
        return "Something went wrong - please try again."


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
    # ID for channel message received from
    channel_id = message["channel"]
    
    # If no chain exists for this channel, create new one
    if not channel_id in THREADS_DICT:
        build_chain(channel_id)
    
    # Store user_message and get bot response
    bot_message = add_chain_link(channel_id, message, loc="apps")
    # Send generated response back to Slack
    say(bot_message)


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
    # ID for channel message received from
    channel_id = body["event"]["channel"]
    
    # If no chain exists for this channel, create new one
    if not channel_id in THREADS_DICT:
        build_chain(channel_id)
    
    # Store user_message and get bot response
    bot_message = add_chain_link(channel_id, body, loc="mentions")
    # Send generated response back to Slack
    say(bot_message)


# ====================================
# Initialisation
# ====================================

if __name__ == "__main__":
    # Create an app-level token with connections:write scope
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
