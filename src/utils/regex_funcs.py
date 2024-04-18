# -*- coding: utf-8 -*-
import re


def re_get_mentions(raw_text: str) -> str:
    """
    Extracts user and bot mentions from message
    """
    pattern = r"<@([A-Z0-9]{9,11})>"
    # Find all matches
    matches = re.findall(pattern, raw_text)
    
    return matches


def re_slack_id(raw_text: str) -> str:
    """
    Removes Slack user ID from start of message (if applicable)
    """
    # Slack user ID format (optional colon and whitespace)
    pattern = r"(<@[A-Z0-9_]{9,11}>)"  
    match = re.match(pattern, raw_text)
    if match:
        # Return remaining raw_text after user ID
        return raw_text[match.end():]  
    # Return original raw_text if no user ID found
    return raw_text  


def re_user_prefixes(raw_text: str) -> str:
    """
    Removes prefixes from printed message responses
    """
    # Remove "AI:" and "AI Assistant:" prefixes
    clean_text = re.sub(r"^(AI\:|\s+AI Assistant\:)(.*)", r"\2", raw_text)
    
    return clean_text


def re_whitespace(raw_text: str) -> str:
    """
    Converts whitespace characters to regular spaces
    """
    # Replace all whitespace with single space
    clean_text = re.sub(r"\s+", " ", raw_text)
    # Remove leading and trailing whitespace
    clean_text = clean_text.strip()
        
    return clean_text


def regex_handler(raw_text: str) -> str:
    """
    Passes user and bot messages to regex functions
    """
    rgx_msg = re_slack_id(raw_text)
    rgx_msg = re_whitespace(rgx_msg)
    rgx_msg = re_user_prefixes(rgx_msg)
    
    return rgx_msg

