'''
File: PLUMGEN_main.py
'''

import logging
import logging.config
from tkinter import messagebox
from controller.PLUMGEN_controller_gen import PlumgenControllerGen
from logger_config import setup_logging


setup_logging() # setup logging


def show_error_message(message, max_length=200):
    if len(message) > max_length:
        truncated_message = message[:max_length] + "..."
    else:
        truncated_message = message
    messagebox.showerror("Error", f"{truncated_message}\n\nIf you're struggling to resolve this error, please share the 'plumgen.log' file with the dev.", master=None)


if __name__ == "__main__":
    try:
        # create the controller instance
        controller = PlumgenControllerGen()
    except Exception as e:
        logging.exception("Main crashed. Error: %s", e) # log the exception
        show_error_message("An error occurred: {}".format(str(e)))