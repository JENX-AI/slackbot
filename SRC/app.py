import together
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App


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
    # query = user_message
