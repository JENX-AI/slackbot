# -*- coding: utf-8 -*-
import os
import openai
from dotenv import load_dotenv
from utils.regex_funcs import regex_handler
from utils.config import (
    MODEL, MAX_TOKENS, SYSTEM_PROMPT,
    TEMPERATURE, THREADS_DICT, TOP_P, VERBOSE
)
from utils.logger import get_logger
# Credentials
load_dotenv()
TOGETHER_API_KEY = os.environ["TOGETHER_API_KEY"]

logger = get_logger(__name__)

# ====================================
# LLM Model
# ====================================

client = openai.OpenAI(
    api_key=TOGETHER_API_KEY, 
    base_url="https://api.together.xyz/v1"
)

# ====================================
# ConversationChain
# ====================================

def build_chain(thread_id: str) -> None:
    """
    Creates memory chain upon first mention of bot
    """
    memory = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Add memory to dict
    THREADS_DICT[thread_id] = memory
    

def add_chain_link(thread_id: str, msg: dict, loc: str) -> str:
    """
    Adds memory chain link for latest message round
    Gets and returns bot response
    """
    # Extract user message from Slack event
    if loc == "apps":
        msg_txt = msg["text"]
    elif loc == "mentions":
        msg_txt = msg["event"]["text"]
    
    try:
        # Clean user message with regex
        rgx_msg = regex_handler(msg_txt)
        
        # Update memory with user message
        memory = THREADS_DICT[thread_id]
        memory.append({"role": "user", "content": rgx_msg})
        
        if VERBOSE:
            print(memory)
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=memory,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            extra_body={"stop_token_ids": [7]}
        )
        bot_msg = response.choices[0].message.content
        # Clean bot message with regex
        rgx_msg = regex_handler(bot_msg)
        # Update memory with bot message
        memory.append({"role": "assistant", "content": rgx_msg})
        
        THREADS_DICT[thread_id] = memory
        
        if VERBOSE:
            print(memory)
        
        return rgx_msg
    
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return "Something went wrong - please try again."
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return "Something went wrong - please try again."

