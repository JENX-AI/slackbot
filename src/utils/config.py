# -*- coding: utf-8 -*-
import os
from utils.system_prompts import SYSTEM_PROMPTS_DICT

# ====================================
# Model selection for cloud
# ====================================

MODELS = {
    "Llama-2-13b-chat-hf": "meta-llama/Llama-2-13b-chat-hf", 
    "Mistral-7B-Instruct-v0.1": "mistralai/Mistral-7B-Instruct-v0.1", 
    "alpaca-7b": "togethercomputer/alpaca-7b", 
    "Yi-34B-Chat": "zero-one-ai/Yi-34B-Chat",
    # Image model
    "stable-diffusion-2-1": "stabilityai/stable-diffusion-2-1",
}
# Get name of repo parent directory
script_path = os.path.abspath(__file__)
# Split path name into components
path_components = script_path.split(os.path.sep)
"""
The end components of the config.py path string are as follows:
{parent directory}/slackbot/src/utils/config.py
"""
if path_components[-5] in MODELS:
    MODEL = MODELS[path_components[-5]]
else:
    # Use LLaMA-2 as default
    MODEL = MODELS["Llama-2-13b-chat-hf"]

# ====================================
# Model manual override for development
# ====================================

# MODEL = "meta-llama/Llama-2-13b-chat-hf"
# MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
# MODEL = "togethercomputer/alpaca-7b"
# MODEL = "zero-one-ai/Yi-34B-Chat"
# IMAGE_MODEL = "stabilityai/stable-diffusion-2-1"

# Select system prompt based on model in use
SYSTEM_PROMPT = SYSTEM_PROMPTS_DICT[MODEL]

# ====================================
# Model parameters
# ====================================

MAX_TOKENS = 500
TEMPERATURE = 0.1
TOP_K = 5
TOP_P = 0.7
REPETITION_PENALTY = 1.1

# Not in use - for reference only
CHATBOTS = {
    "U06T5FVMMKL": "Yi-34B-Chat"
}
