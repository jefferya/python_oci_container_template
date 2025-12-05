"""
Test Demo
"""

import os
import logging

import python_demo  # assumes src/python_demo.py is on PYTHONPATH


def test_main_logs_info(caplog):
    """Ensure main() logs Python version and UID/GID info."""
    caplog.set_level(logging.INFO)

    # Run the demo main function
    python_demo.main()

    # Check that Python version was logged
    assert any("Python version:" in message for message in caplog.messages)

    # Check that UID/GID info was logged
    uid_gid_str = f"UID:[{os.getuid()}] GID:[{os.getgid()}]"
    assert any(uid_gid_str in message for message in caplog.messages)
