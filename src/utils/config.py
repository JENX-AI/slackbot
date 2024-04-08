# -*- coding: utf-8 -*-
from utils.system_prompts import SYSTEM_PROMPTS_DICT

# MODEL = "meta-llama/Llama-2-13b-chat-hf"
# MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
MODEL = "togethercomputer/alpaca-7b"
# MODEL = "zero-one-ai/Yi-34B-Chat"
# IMAGE_MODEL = "stabilityai/stable-diffusion-2-1"

# Select system prompt based on model in use
SYSTEM_PROMPT = SYSTEM_PROMPTS_DICT[MODEL]

# Set model parameters
MAX_TOKENS = 1024
TEMPERATURE = 0.1
TOP_K = 5
TOP_P = 0.7
REPETITION_PENALTY = 1.1

# Not in use - for reference only
CHATBOTS = {
    "U06S474L338": "csbm-bot",
    "U06T5FVMMKL": "Yi-34B-Chat"
}
