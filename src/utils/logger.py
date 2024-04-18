# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str, log_file: str="error.log", log_level: int=logging.INFO) -> logging.Logger:
    """
    Get logger object with specified name, log file, and log level
    
    Parameters
    ----------
    name : str
        name of the logger
    log_file : 
        path to the log file
    log_level : int
        logging level (default is logging.INFO
    
    Returns
    -------
    logging.Logger : logger object
    """
    # Ensure logs directory exists
    log_dir = os.path.join(os.getcwd(), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Construct log path relative to logs directory
    log_path = os.path.join(log_dir, log_file)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler = RotatingFileHandler(log_path, maxBytes=1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

