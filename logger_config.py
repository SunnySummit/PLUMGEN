'''
File: logger_config.py
'''

import os
import sys
import logging
import logging.config

def setup_logging():
    #logging.config.fileConfig('logging.conf')
    exe_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    conf_path = os.path.join(exe_dir, 'logging.conf')
    if not os.path.exists(conf_path):
        conf_path = 'logging.conf'

    logging.config.fileConfig(conf_path)