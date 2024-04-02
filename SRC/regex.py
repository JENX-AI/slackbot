# -*- coding: utf-8 -*-
import re

    
def re_slack_id(raw_text: str) -> str:
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


def re_whitespace(raw_text: str) -> str:
    """
    Converts whitespace characters to regular spaces
    Called by add_chain_link()
    """
    # Replace all whitespace with single space
    clean_text = re.sub(r"\s+", " ", raw_text)
    # Remove leading and trailing whitespace
    clean_text = clean_text.strip()
        
    return clean_text


def re_user_prefixes(raw_text: str) -> str:
    """
    Removes prefixes from printed message responses
    Called by add_chain_link()
    """
    # Remove "AI:" and "AI Assistant:" prefixes
    clean_text = re.sub(r"^(AI\:|\s+AI Assistant\:)(.*)", r"\2", raw_text)
    
    return clean_text

    