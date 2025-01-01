#!/usr/bin/env python3

import os
import sys
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create file handler for logging to a file
file_handler = logging.FileHandler('system_analysis.log')
file_handler.setLevel(logging.DEBUG)  # Write all logs (DEBUG and higher) to the file

# Create a formatter and attach it to the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Set the logger's level to DEBUG to capture all log levels
logger.setLevel(logging.DEBUG)

class ScreenManager:
    def __init__(self):
        self.clear_command = 'cls' if os.name == 'nt' else 'clear'
        logger.debug(f"Clear command set to: {self.clear_command}")

    def clear_screen(self):
        try:
            logger.info(f"Attempting to clear the screen using command: {self.clear_command}")
            os.system(self.clear_command)
            logger.info("Screen cleared successfully.")
        except OSError as e:
            logger.error(f"Error clearing the screen: {e}")
        except KeyboardInterrupt:
            logger.warning("Process interrupted by the user.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"An error occurred while clearing the screen: {e}")
