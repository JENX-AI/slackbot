# -*- coding: utf-8 -*-
import os, logging
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain_together import Together

# Regex functions
from utils.regex import regex_handler
# Constants
from utils.config import SYSTEM_PROMPT, MODEL, MAX_TOKENS, TEMPERATURE
from utils.config import TOP_K, TOP_P, REPETITION_PENALTY
# Credentials
load_dotenv()
TOGETHER_API_KEY = os.environ["TOGETHER_API_KEY"]

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
# ConversationChain
# ====================================

def build_chain(thread_id: str) -> None:
    """
    Creates conversation chain upon first mention of bot
    Called by message_handler() and handle_app_mention_events()
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
    Called by message_handler() and handle_app_mention_events()
    """
    # Extract user message from Slack event
    if loc == "apps":
        msg_txt = msg["text"]
    elif loc == "mentions":
        msg_txt = msg["event"]["text"]
    
    try:
        # Clean user message with regex
        rgx_msg = regex_handler(msg_txt)
        # Generate bot response
        bot_msg = THREADS_DICT[thread_id]["chain"].predict(input=rgx_msg)
        # Clean bot message with regex
        rgx_msg = regex_handler(bot_msg)
        
        return rgx_msg
    
    except KeyError as e:
        logger.error(f"KeyError for THREADS_DICT: {e}")
        return "Something went wrong - please try again."
    
