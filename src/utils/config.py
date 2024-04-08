# -*- coding: utf-8 -*-

MODEL = "meta-llama/Llama-2-13b-chat-hf"
# MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
# MODEL = "togethercomputer/alpaca-7b"
# MODEL = "zero-one-ai/Yi-34B-Chat"
# IMAGE_MODEL = "stabilityai/stable-diffusion-2-1"

MAX_TOKENS = 1024
TEMPERATURE = 0.1
TOP_K = 5
TOP_P = 0.7
REPETITION_PENALTY = 1.1

SYSTEM_PROMPT = """
<s>[INST]<<SYS>>
You are an AI assistant having a conversation with a human.
Use concise and professional language to respond.
Respond directly, do not thank the human for their question when you reply.
If you do not know the answer to a question, state truthfully that you do not know.

{history}<</SYS>>
{input}[/INST]
"""

# Not in use - for reference only
CHATBOTS = {
    "U06S474L338": "csbm-bot"
}
