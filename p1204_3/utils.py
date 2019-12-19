#!/usr/bin/env python3
import os
import sys
import logging

def assert_file(filename, fail_message):
    if not os.path.isfile(filename):
        logging.error(fail_message)
        sys.exit(0)
