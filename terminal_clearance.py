#!/usr/bin/env python3

import os
import sys
import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG,  # Log all levels (DEBUG and above)
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Create a logger
logger = logging.getLogger(__name__)

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
