#!/usr/bin/env python3
import os
import sys
import logging


def assert_msg(check, fail_message):
    if not check:
        logging.error(fail_message)
        sys.exit(0)


def assert_file(filename, fail_message):
    assert_msg(os.path.isfile(filename), fail_message)
