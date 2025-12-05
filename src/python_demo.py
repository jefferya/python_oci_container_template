#!/usr/bin/env python3
########################################
# Desc: AI generated Python Demo for testing output
#
# Usage:
#       python3 python_demo.py --help
#
####################################3333

import argparse
import logging
import os
import sys

def main():
    parser = argparse.ArgumentParser(
            description="Demo script with configurable logging level"
            )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
    )
    args = parser.parse_args()

    # Configure logging based on argument
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.debug("Debugging details enabled")
    logging.info("Python version: %s", sys.version)
    logging.info("Current User: UID:[%s] GID:[%s]", os.getuid(), os.getgid())
    logging.warning("This is a warning example")
    logging.error("This is an error example")
    logging.critical("Critical issue example")

if __name__ == "__main__":
    main()
